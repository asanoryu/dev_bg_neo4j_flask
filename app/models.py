from uuid import uuid4
from datetime import datetime
from typing import List

from passlib.hash import bcrypt

from app.graph import graph


class User:
    def __init__(self, username: str):
        self.username = username

    def find(self) -> List[dict]:
        """Helper to check if user with username exists."""
        res = graph.run(
            "MATCH (u:User {username: $username}) RETURN u LIMIT 1",
            username=self.username,
        )
        return res.data()

    def register(self, password: str) -> bool:
        """Check if user exists and if not create it with the given password."""
        if not self.find():
            res = graph.run(
                "CREATE (_:User {username: $username, password: $password, id:$id})",
                username=self.username,
                password=bcrypt.encrypt(password),
                id=uuid4().hex,
            )
            return True
        else:
            return False

    def verify_password(self, password: str) -> bool:
        """Check if `password` matches for the given user."""
        user = self.find()
        if user:
            return bcrypt.verify(password, user[0]["u"]["password"])
        else:
            return False

    def follow_user(self, other_username: str) -> None:
        """Match the requested user and create a FOLLOWING relationship between us and them."""
        graph.run(
            """MATCH (me:User {username: $me}) 
            MATCH (u2:User {username: $username})  
            MERGE (me)-[r:FOLLOWING {since: datetime($since)}]->(u2)""",
            me=self.username,
            username=other_username,
            since=datetime.now().strftime("%Y-%m-%d"),
        )

    def get_number_of_followed(self) -> int:
        res = graph.run(
            """MATCH (:User {username: $username})-[:FOLLOWING]->(f:User) return count(f)""",
            username=self.username,
        )
        res = res.data()
        return int(res[0]["count(f)"]) if res else 0

    def add_post(self, text: str) -> None:
        """Create a Post node and a POSTED relationship."""
        graph.run(
            """
                MATCH (u:User {username: $username}) 
                CREATE (p:Post {content: $content})
                CREATE (u)-[:POSTED {posted_on: datetime($on)}]->(p)
            """,
            username=self.username,
            content=text,
            on=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        )


def get_recent_posts(username):
    """Get all posts by users we follow and our own posts."""
    res = graph.run(
        """
            MATCH (u:User {username: $username})-[*1..2]->(p:Post)
            WITH p
            MATCH (p)<-[po:POSTED]-(poster:User)
            RETURN poster.username as poster, p.content as content, po.posted_on as posted_on
            ORDER BY posted_on DESC
        """,
        username=username,
    )
    return [
        {
            "poster": row["poster"],
            "content": row["content"],
            "posted_on": row["posted_on"],
        }
        for row in res
    ]


def get_most_followed() -> List[dict]:
    """Return a list of the 10 most followed users and the number of people that follow them."""
    res = graph.run(
        """
            MATCH (u:User)<-[r:FOLLOWING]-(:User)
            RETURN u.username as suggestion, count(r) as followedBy
            ORDER BY followedBy DESC 
            LIMIT 10"""
    )
    return [
        {"username": row["suggestion"], "followed_by": row["followedBy"]} for row in res
    ]


def recommended_people(username):
    """Return a list of users followed by users the user with username is following.
        AKA friends of friends.
    """
    res = graph.run(
        """
        MATCH (u:User)-[:FOLLOWING]->(:User)-[:FOLLOWING]->(ff:User)
        WHERE NOT 
            (u)-[:FOLLOWING]->(ff)
            AND u.username = $username
        RETURN ff.username as suggestion,count(ff) as friendsInCommon
        ORDER BY friendsInCommon DESC
         """,
        username=username,
    )
    return [
        {"username": row["suggestion"], "followed_by": row["friendsInCommon"]}
        for row in res
    ]
