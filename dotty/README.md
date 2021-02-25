# What ? #

Simple flask docker which listen http port 5000 and generate png diagram from dotty plaintext.


# run container #

docker run --rm -i -t -p 5000:5000 --name dotty dotty

# example to use client #

python sample_client.py < hello.dot
