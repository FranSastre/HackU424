#!/bin/bash

/usr/bin/mongod --fork --logpath /var/log/mongodb.log

echo "Waiting for MongoDB to start..."
until mongosh --eval 'db.adminCommand("ping")' | grep -q '"ok" : 1'
do
    sleep 1
done

mongosh <<EOF
use challenge
db.createCollection("users")
db.users.insertOne({username: 'admin', password: '23a52f2902720d27c64bd1a6f797cd65'})
quit()
EOF

/usr/bin/python3 /app/app.py
