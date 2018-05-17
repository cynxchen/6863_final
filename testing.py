from sentence_check import *

def test_print (q, a, exp):
    print ()
    print ("Question: ", q)
    print ("Indirect Answer: ", a)
    print ("* Expected: ", exp)
    result = compare_sentences(q, a)
    print ("* Actual: ", result)
    print ("* MATCH?: ", exp == result)

#answer needs to be same structure. (subj subj, verb, verb)
print ("--- EXAMPLE SENTENCES ---")
test_print("Did the not green penguin eat", "The really green penguin ate.", "No.")
test_print("Is it true that the not cute penguin runs fast", "The cute penguin runs fast", "No.")
test_print("Is it true that the young penguins are really cute?", "All little birds are really cute", "Yes.")
test_print("Do some penguins read books about sports daily?", "Every animal in the northern hemisphere reads books about sports daily.", "Yes.")
test_print("Does the yellow flute make on the table the music", "The blue flute creates on the table the sound.", "Yes.")
test_print("Is it true that he finds penguins", "Penguins find him.", "No.")
test_print("Is it true that humans climb trees?", "Every man has climbed a tree before.", "Yes.")
test_print("Is it true that bears from the forest eat?", "The bears from the forest eat honey.", "Yes.")
test_print("Did the primary students finish their homework?", "Only the secondary students completed their assignments.", "No.")
test_print("Is it true that the hare always runs quick?", "The hare never runs slow.", "Yes.")

#TESTING SET
print ()
print ("--- TEST SET SENTENCES ---")
test_print("Did the automobile get stopped by the police today?", "The car with the blinkers got stopped today.", "Yes.")
test_print("Is it true that the girl's favorite show is on the Discovery channel?", "Her favorite channel is the Disney channel.", "No.")
test_print("Is it true that your favorite type of chocolate is not dark chocolate?", "My favorite type of chocolate is milk chocolate with caramel.", "Yes.")
test_print("Does the alarm never go off?", "The emergency alarm went off this morning.", "No.")
test_print("Is it true that the lady's clothing is very beautiful?", "The girl's dress is really pretty.", "Yes.")
test_print("Is it true that the warm weather makes her sad?", "She's very glad the weather is warm.", "No.")
test_print("Does the pupil use many hyphenations in her writing?", "The student uses a lot of hyphenation in her essays.", "Yes.")
test_print("Did some people go to the event in the city?", "Everyone went to the mixer in Boston today.", "Yes.")
test_print("Is it true that the winners of the competition did not receive a trophy?", "The prize for the competition was a trophy.", "No.")
test_print("Did the boss give promotions to the employees yesterday?", "His boss gave him a promotion today.", "No.")
test_print("Is it true that his interests are in sports?", "The hobby of the agent is football.", "Yes.")
test_print("Did the coach tell your grandmother to exercise?", "A coach told my granny to visit the new room.", "No.")
test_print("Have his organs been making sounds?", "His intestines make sound when he is hungry.", "Yes.")
test_print("Does the obligation of the student depend on the teacher?", "The obligation of the teacher depends on the student.", "No.")
test_print("Do all insecure banks not ask for passwords?", "Every secure bank account asks for a password.", "Yes.")
test_print("Have the wasp sting the boy on the arm?", "Yesterday the wasp stung the boy on the nose.", "No.")
test_print("Does every animal roll?", "Some armadillos rolls around on the grass.", "No.")
test_print("Is it true that punctuation is used in many essays?", "The semicolon is used a lot in papers.", "Yes.")
test_print("Does the author of the book write many books for kids?", "The author of the book is very famous for writing children books.", "Yes.") #YES/NO
test_print("Does the blind woman walk around the city with no issue?", "A blind man walked around the city with no problem.", "No.") #NO/NO
test_print("Does the activity involve music or dancing?", "The favorite activity of the senior involves music.", "Yes.")#YES/NO
test_print("Is it true that the eraser shape tells us something?", "The shape of the eraser tells us how long he has been using it.", "Yes.")#YES/YES
test_print("Did the girls want to go to the zoo today?", "The stepdaughters wanted to go to the park.", "No.")#NO/NO
test_print("Is it true that he likes to wear the top-hat?", "His favorite article of clothing is the top-hat.", "Yes.")#YES/NO
test_print("Does every word matter?", "Not every word in the abstract is very important.", "Yes.")#YES/PARSING error
test_print("Is it true that the restaurant had a sale?", "The mall has a sale today.", "No.")#NO/NO
test_print("Do some assistants help others?", "Every assistant provides assistance as well as they can.", "Yes.")#YES/NO
test_print("Is it true that the main attraction is not the scary ride?", "The main attraction of the park is the scary purple rollercoaster.", "No.")#NO/NO
test_print("Does the bird give birth to cows?", "A bird does not give birth to calves.", "No.")#NO/NO
test_print("Has the coat been hiding in the closet?", "The jacket usually hides inside the closet", "Yes.")#Yes/NO
test_print("Does the ten mile run requires dedication?", "The five mile run requires a lot of dedication.", "Yes.")#YES/NO
test_print("Did the girl defeat the boss to go to the next level?", "A boy defeated the boss to advance to the next level. ", "No.")#NO/NO
test_print("Do all elephants run for president?", "Male elephants do not run for president.", "No.")#NO/NO
test_print("Will the parade leader trip on the wire?", "The leader of the parade tripped on the wire for the microphone.", "Yes.")
test_print("Does the worker always put tiles together?", "A house builder sometimes lays tiles on the floor.", "No.")
