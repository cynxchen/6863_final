from sentence_check import *

#answer needs to be same structure. (subj subj, verb, verb)
print (compare_sentences("Did the not green penguin eat", "The really green penguin ate."))
print (compare_sentences("Is it true that the not cute penguin runs fast", "The cute penguin runs fast"))
print (compare_sentences("Is it true that the young penguins are really cute?", "All little birds are really cute"))
print (compare_sentences("Do some penguins read books about sports daily?", "Every animal in the northern hemisphere reads books about sports daily."))
print (compare_sentences("Does the yellow flute make on the table the music", "The blue flute creates on the table the sound."))
print (compare_sentences("Is it true that he finds penguins", "Penguins find him."))
print (compare_sentences("Is it true that humans climb trees?", "Every man has climbed a tree before."))
print (compare_sentences("Is it true that bears from the forest eat?", "The bears from the forest eat honey."))
print (compare_sentences("Did the primary students finish their homework?", "Only the secondary students completed their assignments."))
print (compare_sentences("Is it true that the hare always runs quick?", "The hare never runs slow."))

#TESTING SET
print (compare_sentences("Did the automobile get stopped by the police today?", "The car with the blinkers got stopped today."))
print (compare_sentences("Is it true that the girl’s favorite show is on the Discovery channel?", "Her favorite channel is the Disney channel."))
print (compare_sentences("Is it true that your favorite type of chocolate is not dark chocolate?", "My favorite type of chocolate is milk chocolate with caramel."))
print (compare_sentences("Does the alarm never go off?", "The emergency alarm went off this morning."))
print (compare_sentences("Is it true that the lady’s clothing is very beautiful?", "The girl’s dress is really pretty."))
print (compare_sentences("Is it true that the warm weather makes her sad?", "She’s very glad the weather is warm."))
print (compare_sentences("Does the pupil use many hyphenations in her writing?", "The student uses a lot of hyphenation in her essays."))
print (compare_sentences("Did some people go to the event in the city?", "Everyone went to the mixer in Boston today."))
print (compare_sentences("Is it true that the winners of the competition did not receive a trophy?", "The prize for the competition was a trophy."))
print (compare_sentences("Did the boss give promotions to the employees yesterday?", "His boss gave him a promotion today."))
print (compare_sentences("Is it true that his interests are in sports?", "The hobby of the agent is football."))
print (compare_sentences("Did the coach tell your grandmother to exercise?", "A coach told my granny to visit the new room."))
print (compare_sentences("Have his organs been making sounds?", "His intestines make sound when he is hungry."))
print (compare_sentences("Does the obligation of the student depend on the teacher?", "The obligation of the teacher depends on the student."))
print (compare_sentences("Do all insecure banks not ask for passwords?", "Every secure bank account asks for a password."))
print (compare_sentences("Have the wasp sting the boy on the arm?", "Yesterday the wasp stung the boy on the nose."))
print (compare_sentences("Does every animal roll?", "Some armadillos rolls around on the grass."))
print (compare_sentences("Is it true that punctuation is used in many essays?", "The semicolon is used a lot in papers."))#YES/NO
print (compare_sentences("Does the author of the book write many books for kids?", "The author of the book is very famous for writing children books.")) #YES/NO
print (compare_sentences("Does the blind woman walk around the city with no issue?", "A blind man walked around the city with no problem.")) #NO/NO
print (compare_sentences("Does the activity involve music or dancing?", "The favorite activity of the senior involves music."))#YES/NO
print (compare_sentences("Is it true that the eraser shape tells us something?", "The shape of the eraser tells us how long he has been using it."))#YES/YES
print (compare_sentences("Did the girls want to go to the zoo today?", "The stepdaughters wanted to go to the park."))#NO/NO
print (compare_sentences("Is it true that he likes to wear the top-hat?", "His favorite article of clothing is the top-hat."))#YES/NO
print (compare_sentences("Does every word matter?", "Not every word in the abstract is very important."))#YES/PARSING error
print (compare_sentences("Is it true that the restaurant had a sale?", "The mall has a sale today."))#NO/NO
print (compare_sentences("Do some assistants help others?", "Every assistant provides assistance as well as they can."))#YES/NO
print (compare_sentences("Is it true that the main attraction is not the scary ride?", "The main attraction of the park is the scary purple rollercoaster."))#NO/NO
print (compare_sentences("Does the bird give birth to cows?", "A bird does not give birth to calves."))#NO/NO
print (compare_sentences("Has the coat been hiding in the closet?", "The jacket usually hides inside the closet"))#Yes/NO
print (compare_sentences("Does the ten mile run requires dedication?", "The five mile run requires a lot of dedication."))#YES/NO
print (compare_sentences("Did the girl defeat the boss to go to the next level?", "A boy defeated the boss to advance to the next level. "))#NO/NO
print (compare_sentences("Do all elephants run for president?", "Male elephants do not run for president.", True))#NO/NO
print (compare_sentences("Will the parade leader trip on the wire?", "The leader of the parade tripped on the wire for the microphone."))
print (compare_sentences("Does the worker always put tiles together?", "A house builder sometimes lays tiles on the floor."))
