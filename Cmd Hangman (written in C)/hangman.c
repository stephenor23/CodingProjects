#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#define MAXCHAR 1000
#define RANDMAX 10

char* get_title(); // finds a title randomly from the provided txt file of movie titles
char to_lower_case(char c); // returns the given letter in lower case (changes nothing if arg isn't upper case letter)
char get_guess();			// asks user for a char and returns it
void get_stars(char* s);	// turns each letter in a string into a *
bool is_valid_guess(char* t, char g); 	// checks if a guess is correct
void update_stars(char*t, char* s, char c);	// replaces every '*' in s, with the char c
bool is_complete(char* s);	// returns true when the game is complete

int main(){

	printf("\n\n\t\t___ GUESS THE TITLE OF THE MOVE ___\n\n");

	bool won = true;  // the value here will determine the output when the game is over
	int lives = 5;  // the user has five guesses, this will be decremented each time they guess incorrectly

	char *title;  	// string containing the title of the movie i.e. the answer
	title = get_title();  

	char stars[40];  // this will only show the letters that the user has guessed correctly
	strcpy(stars, title);  // this will initially have the same value as "title", but we will "hide" the letters behind '*'s

	get_stars(stars);  // edit the stars string to show asterisks instead of letters
	char user_guess;  // users guess will be saved here


	printf("\n%s\n%s\ntx", title, stars); // test

	while (is_complete(stars) == false){  // keep going until the user reveals all the letters 
											// (or break when they're out of lives) 

		if (lives < 1){ // if the user has run out of lives
			won = false;  // user has lost
			break;  // exit the loop, as we're not taking any more user input
		}

		// show unfinished string and no. of lives left to user
		printf("\n\n%s\n", stars);
		printf("You have %i lives left.\n", lives);

		user_guess = get_guess();  // get a guess from the user

		// check if the user's guess is correct
		if (is_valid_guess(title, user_guess)){
			printf("Your guess was correct!\n");
			update_stars(title, stars, user_guess);  // reveal the correct letters
		}
		else{  // if the user's guess is incorrect
			printf("You guess was NOT correct!\n");
			lives--; // user loses a life
		}

	} // at the end of this loop, we will know if the user has won or lost the game


	if (won){
		printf("\nCongratulations, the answer was %s\n", title); // user has won
	}
	else{
		printf("\n___GAME OVER___\nYou have run out of lives.\nThe answer was %s\n", title); // user has lost
	}

}


char * get_title(){

	srand(time(NULL));  // initialises random number generator
	int r = rand()%RANDMAX;  // we only want a number between 0 and 9

	char *s = malloc(10000); // allocate memory for the string we'll be returning

	FILE *fp;  // file pointer
	char str[MAXCHAR]; 
	char* filename = "./movies.txt";  // file containing movie titles

	fp = fopen(filename, "r");

	int count = 0;
	while (fgets(str, MAXCHAR, fp) != NULL){
		if (count == r){  // select the line chosen by the random number generator
			s = str;
			s[strlen(s)-1] = '\0';  // remove the '\n' at the end of the
			break;
		}
		count++; // increment count of loop iterations
	}

	fclose(fp);  // close the file

	return s;
}


char to_lower_case(char c){
	if (c >= 65){  
		if (c <= 90){  // if c has ASCII value between 65 and 90 then it is an upper case letter
			return c + 32; // changes its ASCII value to that of the corresponding lower case letter
		}
	}
	return c;  // changing the letter wasn't necessary, return it as passed
}

char get_guess(){
	char guess;
	printf("Enter a letter to guess: ");  // prompt
	scanf(" %c", &guess);  // get input

	return to_lower_case(guess);  // return the input in lower case
}

void get_stars(char* s){
	for (int i=0; i<strlen(s); i++){  // iterate through each char in the string
		if (s[i] != ' '){
			s[i] = '*';  // turn every character except space characters into a '*'
		}
	}
}

bool is_valid_guess(char* t, char g){

	for (int i=0; i<strlen(t); i++){  // iterate through every char in the string
		if (g == to_lower_case(t[i])){  // if the user's guess appears in the string
			if (g != ' '){  // ensure the user hasn't made an invalid guess
				return true;
			}
		}
	}

	return false;  // user's guess wasn't found in the title and is therefore incorrect
}

void update_stars(char*t, char* s, char c){  // this function is called when we already know that c is a correct guess

	for (int i=0; i<strlen(s); i++){  // iterate though every char in 'hidden letters' string
		if (to_lower_case(t[i]) == c){  // here i is a position in the string where c is correct
			s[i] = t[i];  // replace the '*' with the correct letter
		}
	}
}

bool is_complete(char* s){ // check if there are no more '*'s in the hidden-letters string, i.e. the user has gotten every letter
	for (int i=0; i<strlen(s); i++){
		if (s[i] == '*'){  // if we find an asterisk
			return false;  // then the game isn't complete
		}
	}
	return true;  // we have traversed the whole string without finding an asterisk, therefore the user has found every letter
}
