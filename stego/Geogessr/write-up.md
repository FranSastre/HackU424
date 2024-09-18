# Geogessr

## Category

Geogessr

## Dificulty

Easy

## Challenge Description

When you are thirsty and stranded in the desert it's not easy to find the right spot to order some drinks. The attached image may help you.

## Hints

- {LEVEL 1} Look into the image metadata.
- {LEVEL 2} The additional information is encoded in BASE64.

## Solution

The image contains 2 BASE64 encoded strings in the metadata.

The Caption-Abstract metadata contains a clue on how to compose the flag:
'ZmxhZyBpcyBIYWNrNFV7ICsgTmFtZSBvZiB0aGUgcGxhY2UgKyB9' --> 'flag is Hack4U{ + Name of the place + }'

The By-lineTitle data contains the coordenates of the place:
'LTI2LjA3MDAyMzMsMTM1LjI0NzEzMzQsMTcuMjV6' --> '-26.0700233,135.2471334,17.25z'

The coordinates take you to the Mt Dare Hotel in Australia

[Mt Date Hotel](https://www.google.com/maps/@-26.0700329,135.2471441,17z)

## Flag

HACK4U{MtDareHotel}