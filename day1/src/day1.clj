(ns day1
  (:require [clojure.string :as str])
  (:import (java.lang Character)))

(def input (slurp "./input.txt"))

(def sample "1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet")

(def sample2 "two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen")

(def digits-word (str/split "zero one two three four five six seven eight nine" #" "))
(def digits (str/split "0123456789" #""))

(defn starts-witn-num [s num]
  (or (str/starts-with? s (get digits num))
      (str/starts-with? s (get digits-word num))))

(defn str-nums [s] ;really inefficient but good enough for the puzzle 
  (mapcat (fn [si] (filter (fn [i] (starts-witn-num (subs s si) i)) (range 10)))  (range (count s))))

(defn solve-part2 [input]
  (->> input
       (str/split-lines)
       (mapv str-nums)
       (map (partial (juxt first last)))
       (map #(+ (* 10 (first %)) (last %)))
       (apply +)))

(comment
  (solve-part2 sample2) ; 281
  (solve-part2 input) ; 54208
  )

(defn solve-part1 [input]
  (->> input
       (str/split-lines)
       (mapv (partial filterv #(Character/isDigit %)))
       (mapv #(vector (first %) (last %)))
       (map str/join)
       (map parse-long)
       (apply +)))

(comment
  (solve-part1 sample) ; 142
  (solve-part1 input) ; 54940
  )
