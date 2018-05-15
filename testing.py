from sentence_check import *

#answer needs to be same structure. (subj subj, verb, verb)
print (compare_sentences("Did the not green penguin eat", "The really green penguin ate."))
print (compare_sentences("Is it true that the not cute penguin runs fast", "The cute penguin runs fast"))
print (compare_sentences("Is it true that the young penguins are really cute?", "All little birds are really cute"))
print (compare_sentences("Do some penguins read books about sports daily?", "Every animal in the northern hemisphere reads books about sports daily."))
print (compare_sentences("Does the yellow flute make on the table the music", "The blue flute creates on the table the sound."))
print (compare_sentences("Is it true that he finds penguins", "Penguins find him."))
print (compare_sentences("Is it true that humans climb trees?", "Every man has climbed a tree before.")) # dictionary size error ?
print (compare_sentences("Is it true that bears from the forest eat?", "The bears from the forest eat honey."))
print (compare_sentences("Did the primary students finish their homework?", "Only the secondary students completed their assignments."))
print (compare_sentences("Is it true that the hare always runs quick?", "The hare never runs slow."))



#TESTING

print (compare_sentences("Is it true that punctuation is used in many essays?", "The asterisk is used a lot in papers."))
#YES/NO

print (compare_sentences("Does the author of the book write many books for kids?", "The author of the book is very famous for writing children books."))
#YES/NO
print (compare_sentences("Does the blind woman walk around the city with no issue?", "A blind man walked around the city with no problem."))
#NO/NO
print (compare_sentences("Does the activity involve music or dancing?", "The favorite activity of the senior involves music."))
#YES/NO
print (compare_sentences("Is it true that the eraser shape tells us something?", "The shape of the eraser tells us how long he has been using it."))
#YES/YES
print (compare_sentences("Did the girls want to go to the zoo today?", "The stepdaughters wanted to go to the park."))
#NO/NO
print (compare_sentences("Is it true that he likes to wear the top-hat?", "His favorite article of clothing is the top-hat."))
#YES/NO
print (compare_sentences("Does every word matter?", "Not every word in the abstract is very important."))
#YES/PARSING error
print (compare_sentences("Is it true that the restaurant had a sale?", "The mall has a sale today."))
#NO/NO
print (compare_sentences("Do some assistants help others?", "Every assistant provides assistance as well as they can."))
#YES/NO
print (compare_sentences("Is it true that the main attraction is not the scary ride?", "The main attraction of the park is the scary purple rollercoaster."))
#NO/NO
print (compare_sentences("Does the bird give birth to cows?", "A bird does not give birth to calves."))
#NO/NO
print (compare_sentences("Has the coat been hiding in the closet?", "The jacket usually hides inside the closet"))
#Yes/NO
print (compare_sentences("Does the ten mile run requires dedication?", "The five mile run requires a lot of dedication."))
#YES/NO
print (compare_sentences("Did the girl defeat the boss to go to the next level?", "A boy defeated the boss to advance to the next level. "))
#NO/NO
print (compare_sentences("Do all elephants run for president?", "Male elephants do not run for president."))
#NO/NO
