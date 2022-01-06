#!/bin/bash
for i in {0..9}
do
  prosodyctl register "water_monitoring_${i}" localhost 1qaz@WSX ;
  prosodyctl register "fish_content_monitoring_${i}" localhost 1qaz@WSX ;
  prosodyctl register "weather_monitoring_${i}" localhost 1qaz@WSX ;
  prosodyctl register "crowd_monitoring_${i}" localhost 1qaz@WSX ;
done
#
#prosodyctl register test1 localhost 1qaz@WSX ;
#prosodyctl register test2 localhost 1qaz@WSX ;
#prosodyctl register test3 localhost 1qaz@WSX ;
#prosodyctl register receiver localhost 1qaz@WSX ;
#prosodyctl register sender localhost 1qaz@WSX ;
#
#prosodyctl register data_accumulator localhost 1qaz@WSX ;
#prosodyctl register fishery_recommender localhost 1qaz@WSX ;
#prosodyctl register client_reporter localhost 1qaz@WSX ;
#prosodyctl register user localhost 1qaz@WSX ;