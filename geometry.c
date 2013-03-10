/*
 * CS 214
 * Jarek Sedlacek
 * HW 0 (Geometry)
 *
 * Menu and CLI driven program that calculate area, volume, and surface area for various shapes
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//its more convenient to use 'true' and 'false' than 1 and 0
typedef enum boolean{FALSE,TRUE} bool;

/* calculate and display area of a rectangle */
double getRectangleData(double width, double height){
	double area = width*height;
	return area;
}
/* calculate and display area of a circle */
double getCircleData(double radius){
	double area = M_PI * pow(radius,2);
	return area;
}

/* calculates  area of a triangle using Heron's formula */
double getTriangleData(double side1, double side2, double side3){
	double perimiterOverTwo = (side1+side2+side3)/2.0;
	double area = sqrt(perimiterOverTwo * (perimiterOverTwo-side1) * (perimiterOverTwo-side2) * (perimiterOverTwo-side3));
	return area;
}
/* calculates  area of a regular polygon */
double getPolygonData(int numSides, double sideLength){
	if (numSides <3){
		return -1;
	}
	double area = ( pow(sideLength,2) * numSides) / (4 * tan(M_PI / numSides));
	return area;
}
/* calculates  volume and surface area of a rectangular box */
double *getBoxData(double height, double width, double depth){
	double volume = height * width * depth;
	double surfaceArea = 2*height*width + 2*width*depth + 2*height*depth;
	double *toReturn = (double*) malloc(sizeof(double) *2);
	toReturn[0] = volume;
	toReturn[1] = surfaceArea;
	return toReturn;
}
/*calculate and display volume and surface area of a cylinder*/
double *getCylinderData(double radius, double height){
	double volume = M_PI * pow(radius,2) * height;
	double surfaceArea = 2*M_PI * pow(radius,2) + M_PI * 2* radius * height;
	double *toReturn = (double*) malloc(sizeof(double) *2);
	toReturn[0] = volume;
	toReturn[1] = surfaceArea;
	return toReturn;
}
/*calculates  volume of surface area of a sphere*/
double *getHemisphereData(double radius){
	double surfaceArea = 4 * M_PI * pow(radius,2);
	surfaceArea /=2;
	surfaceArea += M_PI * pow(radius,2);
	double volume = 4.0 / 3 * M_PI * pow(radius,3);
	volume /=2;
	double *toReturn = (double*) malloc(sizeof(double) *2);
	toReturn[0] = volume;
	toReturn[1] = surfaceArea;
	return toReturn;
}

/*calculates  volume of surface area of a sphere*/
double *getSphereData(double radius){
	double surfaceArea = 4 * M_PI * pow(radius,2);
	double volume = 4.0 / 3 * M_PI * pow(radius,3);
	double *toReturn = (double*) malloc(sizeof(double) *2);
	toReturn[0] = volume;
	toReturn[1] = surfaceArea;
	return toReturn;
}

/*calculates  volume and surface area of a cone*/
double *getConeData(double radius, double height){
	double volume = 1.0 / 3 * M_PI * pow(radius,2) * height;
	double surfaceArea = M_PI * pow(radius,2) +  ( M_PI * radius * sqrt( pow(radius,2) + pow(height,2) ));
	double *toReturn = (double*) malloc(sizeof(double) *2);
	toReturn[0] = volume;
	toReturn[1] = surfaceArea;
	return toReturn;

}
// calculates  volume and surface area of a square pyramid
double *getPyramidData(double baseSideLength, double height){
	double volume = 1.0 / 3 * pow(baseSideLength,2) * height;
	double surfaceArea = baseSideLength * (baseSideLength + sqrt( pow(baseSideLength,2) + 4 * pow(height,2)));
	double *toReturn = (double*) malloc(sizeof(double) *2);
	toReturn[0] = volume;
	toReturn[1] = surfaceArea;
	return toReturn;
}
//calculate area of an ellipse
double getEllipseData(double width, double length){
	double area = M_PI * width/2 * length/2;
	return area;

}
//calculates  volume and surface area of an elliptical cylinder
double *getECylinderData(double width, double length, double height){
	double volume = getEllipseData(width,length) * height;	
	double basePerimiter = 3 * (width/2 + length/2) - sqrt( (3*width/2 + length/2) * (width/2 + 3*length/2));
	double surfaceArea = 2* getEllipseData(width,length) + basePerimiter*height;
	double *toReturn = (double*) malloc(sizeof(double) *2);
	toReturn[0] = volume;
	toReturn[1] = surfaceArea;
	return toReturn;
}


/*
 * This determines which shape the user wants the calculations for, and checks the correct number of arguments were given.
 * It also exits the program if 'quit' was entered
 *
 * It just checks the first word, if it recognizes it as a shape it makes sure the correct number of arguments was entered, then
 *   calls the corresponding function to calculate and display the info
 * if the right number of arguments wasn't entered, it says what the arguments should be for that shape
 *
 * If it doesn't recognize the first word, it tells the user it was invalid input, and returns without doing anything else 
 *
 */
void parseMenuChoice(int argc, char** argv){
	if (strcasecmp(argv[0],"rectangle") == 0){
		if (argc == 3){
			double area = getRectangleData( atof(argv[1]) , atof(argv[2]) );
			printf("Area of the Rectangle: %g\n",area);
		}else{
			fprintf(stderr,"rectangle requires the following arguments: \"rectangle <width> <height>\"\n");	
		}	
	}else if (strcasecmp( argv[0], "circle") == 0){
		if (argc== 2){
			double area = getCircleData( atof(argv[1]) );
			printf("Area of the Circle: %g\n",area);
		}else{
		 	fprintf(stderr,"circle requires the following arguments: \"circle <radius>\"\n");	
		}
	}else if (strcasecmp( argv[0], "triangle") == 0){
		if (argc == 4){
			double area = getTriangleData( atof(argv[1]), atof(argv[2]), atof(argv[3]) );
			if(isnan(area) || area == 0){
				fprintf(stderr,"It is physically impossible for a triangle to exist with side lengths %s %s %s\nArea cannot be computed\n", argv[1], argv[2], argv[3]);
			}else{
				printf("Area the Triangle: %g\n",area);	
			}
		}else{
			fprintf(stderr,"triangle requires the following arguments: \"triangle <side1> <side2> <side3>\"\n");
		}
	}else if (strcasecmp( argv[0], "polygon") == 0){
		if (argc == 3){
			double area = getPolygonData( atoi(argv[1]), atof( argv[2]) );
			if(area != -1){
				printf("Area of Polygon: %g\n", area);
			}else{
				printf("A polygon must have at least 3 sides\n");	
			}
		}else{
			fprintf(stderr, "polygon requires the following arguments: \"polygon <numsides> <sidelength>\"\n");
		}
	}else if (strcasecmp( argv[0], "box") == 0){
		if( argc == 4){
			double *results = getBoxData( atof(argv[1]), atof(argv[2]), atof(argv[3]));
			printf("Volume of the Box: %g, Surface Area of the Box: %g\n",results[0],results[1]);
			free(results);
		}else{
			fprintf(stderr, "box requires the following arguments: \"box <length> <width> <height>\"\n");	
		}
	}else if (strcasecmp( argv[0], "cylinder") == 0){
		if (argc == 3){
			double *results = getCylinderData( atof(argv[1]), atof(argv[2]));
			printf("Volume of the Cylinder: %g, Surface Area of the Cylinder: %g\n",results[0],results[1]);
			free(results);
		}else{
			fprintf(stderr,"cylinder requires the following arguments \"cylinder <radius> <height>\"\n");	
		}
	}else if ( strcasecmp( argv[0], "cone") == 0){
		if (argc == 3){
			double *results = getConeData( atof(argv[1]), atof(argv[2]) );	
			printf("Volume of the Cone: %g, Surface Area of the Cone: %g\n",results[0],results[1]);
			free(results);
		}else{
			fprintf(stderr,"cone requires the following arguments \"cone <radius> <height>\"\n");
		}
	}else if ( strcasecmp( argv[0], "pyramid") == 0){
		if (argc ==3){
			double * results = getPyramidData( atof(argv[1]), atof(argv[2]));
			printf("Volume of the Pyramid: %g, Surface Area of the Pyramid: %g\n",results[0],results[1]);
			free(results);
		}else{
			fprintf(stderr,"pyramid requires the following arguments \"pyramid <base side length> <height>\"\n");
		}
	}else if ( strcasecmp( argv[0], "sphere") == 0){
		if (argc ==2){
			double * results = getSphereData( atof(argv[1]));
			printf("Volume of the Sphere: %g, Surface Area of the Sphere: %g\n",results[0],results[1]);
			free(results);
		}else{
			fprintf(stderr,"sphere requires the following arguments \"sphere <radius>\"\n");
		}
	} else if ( strcasecmp( argv[0], "ellipse") == 0){
		if ( argc == 3){
			double area = getEllipseData( atof(argv[1]), atof(argv[2]));
			printf("Area of the Ellipse: %g\n",area);
		}else{
			fprintf(stderr, "ellipse requires the following \"ellipse <width> <height>\"\n");
		}	
	}else if ( strcasecmp( argv[0], "hemisphere") == 0){
		if (argc ==2){
			double * results = getHemisphereData( atof(argv[1]));
			printf("Volume of the Hemisphere: %g, Surface Area of the Hemisphere: %g\n",results[0],results[1]);
			free(results);

		}else{
			fprintf(stderr, "hemisphere requires the following arugments \"hemisphere <radius>\"\n");
		}
	}else if ( strcasecmp( argv[0], "ecylinder" ) == 0){
		if (argc == 4){
			double * results = getECylinderData( atof(argv[1]) , atof(argv[2]), atof(argv[3]));
			printf("Volume of the ECylinder: %g, Surface Area of the ECylinder: %g\n",results[0],results[1] );
			free(results);
		}else{
			fprintf(stderr,"ecylinder requires the following arguments \"ecylinder <width> <length> <height>\"\n");	
		}
	}else if ( strcasecmp( argv[0] , "quit") == 0 ) {
		printf("Goodbye\n");
		exit(0);
	}else{
		fprintf(stderr,"%s is not a valid shape \n",argv[0]);	
	}
}

/*
 * This just makes sure all the numerical inputs are positive because negative or zero dimensions don't make sense.
 *
 * returns true if all inputs are positive, or false if at least one is not
 */
bool dimensionsArePositive(int argc, char** argv){
	int i;
	for (i =0; i < argc; i++){
		if ( atof(argv[i]) <= 0){
			return FALSE;
		}
	}
	return TRUE;

}
/*
 * This takes a string the user has inputed, and splits it into an array of words
 * each word is defined as whatever is seperated by spaces
 *
 * We do this so we can use the same parseMenuChoice function for cli arguments and user input from the application's prompt
 * (because both forms of input can now be represented as a char**)
 *
 * This takes a char* representing the user's input string, and an address to store the number of tokens found
 *
 * it returns an array of words (as a char**)
 */
char** tokenizeUserInput(char* input, int* numTokens){
	//make sure we start with zero tokens
	*numTokens = 0;
	//we start with only one string allocated, and allocate more for each token we extract
	char** userInputs = (char**) malloc(sizeof(char*));
	userInputs[*numTokens] = (char*) malloc(sizeof(char) * 128);

	//start tokenizer, and grab first token
	userInputs[(*numTokens)++] = strtok(input," \n");

	//this is where we temporarily store each token, so we can check if its null before adding it to userInputs
	char *temp = (char*)malloc(128);

	//now, we loop and pull out tokens until we run out (and break is called)
	while(TRUE){
		//pull out the token
		temp = strtok(NULL," \n");
		//if its valid, make room for it in userInputs, and add it
		if (temp != NULL){
			userInputs = (char**) realloc(userInputs,sizeof(char*) * (*numTokens) + 1);
			userInputs[*numTokens] = (char*) malloc(sizeof (char) * 128);
			strcpy(userInputs[(*numTokens)++],temp);
		//otherwise, break the loop so we can return
		}else{
			break;
		}
	}
	free(temp);
	return userInputs;
}

int main(int argc, char **argv){

	// if the program was run with arguments, instead of showing the menu just use the arguments as input	
	// this lets the user test it with some script by calling the program once for each line in a file or something 
	// instead of opening the program, and typing each one in 
	if (argc > 1){
		//make sure all dimensions are > 0, complain and exit if they aren't
		//The first two arguments aren't dimensions, they are the program name and shape name, so don't pass them
		if(dimensionsArePositive(argc-2,&argv[2])){
			//we don't need the application name in either argc or argv when we pass them
			parseMenuChoice(argc-1,&argv[1]);	
		}else{
			fprintf(stderr, "Dimensions must be positive real numbers, no calculations were performed\n");	
			return 1;
		}
	//if no arguments were given, go into menu mode
	}else{
		//we continously show the menu, get input, and act on it
		//when parseMenuChoice detects that the user entered 'quit', it calls exit(0)
		while(TRUE){

			//print the menu and prompt
			printf("\nThese are the possible shapes to get data on. Enter one of them too see what arguments are required\n\n");
			printf("Box\tRectangle\tPolygon\t\tCylinder\tEllipse\t\tPyramid\n");
			printf("Cone\tTriangle\tCircle\t\tECylinder\tSphere\t\tHemisphere\n");
			printf("\nOr type \'quit\' to exit");
			printf("\n\n> ");

			//since the only needed input is a shape name and dimensions, 128 chars is plenty	
			unsigned int size = 128;
			char *input = (char*) malloc(size * sizeof(char));

			//read in a line of input from the user
			fgets(input,size,stdin);

			//split that line into an array of words, and a count of the number of words
			int numWords = 0;
			char** tokenizedInput = tokenizeUserInput(input, &numWords);
			//now, we can use the exact same function as we did with commandline arguments, since the input
			//is represented as a char** and a count
			//also, if only 1 word was used as input, we don't have to check if dimensions are positive (because there are none)
			if( ( numWords == 1) || dimensionsArePositive( numWords-1, &tokenizedInput[1])  ){
				parseMenuChoice(numWords,tokenizedInput);	
			}else{
				fprintf(stderr, "Dimensions must be positive real numbers, no calculations were performed\n");	
			}
			//free the memory we allocated in this loop (tokenizedInput[0] winds up pointing to the same place as input
			//so we don't have to explicitely free it, the memory is freed here.)
			int i;
			for(i =0; i < numWords; i++){
				free(tokenizedInput[i]);
			}
			free(tokenizedInput);
		}
	}
	return 0;
}
