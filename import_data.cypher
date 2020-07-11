LOAD CSV FROM "file:///users.csv" as row
WITH row[0] as uid, row[1] as user_name,row[2] as password
CREATE (:User {id: uid, username : user_name, password: password})

CREATE CONSTRAINT ON ()-[following:FOLLOWING]-() ASSERT exists(following.day)

LOAD CSV FROM "file:///relationships.csv" as row
WITH row[0] as uid_1, row[1] as uid_2, datetime(row[2]) as since 
MATCH (u1:User {id:uid_1})
MATCH (u2:User {id:uid_2})
WHERE uid_1 <> uid_2 AND NOT (u1)-[:FOLLOWING]->(u2)
MERGE (u1)-[f:FOLLOWING {since: since}]->(u2)

LOAD CSV FROM "file:///posts.csv" as row
WITH row[0] as uid_1, row[1] as post, datetime(row[2]) as posted_on 
MATCH (u1:User {id:uid_1})
WITH u1 as poster, post, posted_on
MERGE (p:Post {content: post}) 
MERGE (poster)-[:POSTED {posted_on: posted_on}]->(p)