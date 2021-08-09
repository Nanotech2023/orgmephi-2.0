#!/bin/bash

if [ !  -f "id_rsa.pub"  ]
then
  ssh-keygen -t rsa -m PEM -N "" -f id_rsa
fi