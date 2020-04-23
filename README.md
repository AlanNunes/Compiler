# This Is a Programming Language (AN)
It's the first compiler I write. I am building a new own programming language.

|                      | Variables | If/ElseIf/Else | Loop  | Function | Recursion |
| -------------------- |:---------:|:--------------:|:-----:|:--------:|:---------:|
| Runtime      	       | ✔         | ✔             | ✔     | ✔       | ✔	 |
| Code Generation      | ✔         | ✔             | ✔     | ✔       | ✔	 |

# Grammar
[See the grammar here](grammar.txt)

# Requirements
Python version >= 3 ([install python](https://www.python.org/downloads))

# Instructions
Open your bash, got to project's root directory and then type ``python main.py --src tests\fibonacci.an``. Type ``python main.py --help`` to see more options.  
You can write your own algorithm creating a new file ``new_file.an`` and then running it as explained above.

# Code Generation
### source code
```
loop 7:
	print "Hello World"
endloop
```
### is translated to:
```C#
namespace an
{
    class Program
    {
        static void Main()
        {

            for (int i = 0; i < 7; i += 1)
            {
                System.Console.WriteLine("Hello World");
            }

        }
    }
}
```

# Abstract Syntax Tree (AST)
**You can view AST while compiling**
```
-> Statements
      |-> Loop
      |-> VarDeclare
      |______|______|-> x
      |______|-> =
      |______|______|-> Num
      |______|______|______|-> 0
      |______|-> x
      |-> <
      |______|-> Num
      |______|______|-> 10
      |______|-> x
      |-> =
      |______|______|-> x
      |______|-> +
      |______|______|-> Num
      |______|______|______|-> 1
      |-> Statements
      |______|-> Print
      |______|______|-> x
```

# Samples
## Fibonacci
```
declare n = 10
declare t = 0
declare tt = 1
declare nextTerm  = 0
loop declare i = 1; i <= n; i = i + 1:
    if i == 1:
        print t
    elseif i == 2:
        print tt
    endif
    nextTerm = t + tt
    t = tt
    tt = nextTerm
    print nextTerm
endloop
```
**Output**
![Fibonacci](https://i.imgur.com/8OKwqJY.png)

## Hello World
```
print "Hello World"
```
**Output**
![Hello World](https://i.imgur.com/a40WVke.png)

## Collections (array)
**You still cannot change a value from a collection (contribute for this feature!)**
```
declare collection = [1, 2, 3, 4, 5]
append(collection, 6)
loop declare i = 0; i < count(collection); i = i+1:
	print collection[i]
endloop
```
**Output**
![Collections](https://i.imgur.com/A1xgrCC.png)

## While
```
declare x = 0
while x < 10:
	x = x + 1
	print x
elsewhile x < 20:
	x = x + 10
	print x
endwhile
```
**Output**
![While](https://i.imgur.com/pK9yUof.png)


## Loop (for loop)
#### Sample 1
```
loop declare x = 0; x < 10; x = x + 1:
	print x
endloop
```
**Output**
![Loop](https://i.imgur.com/mtdvGOp.png)

#### Sample 2
```
loop declare i = 0; 10:
	print "Hello World " + i
endloop
```
**Output**
![Loop2](https://i.imgur.com/7nVVlt6.png)

#### Sample 3
```
loop 7:
	print "Hello World"
endloop
```
**Output**
![Loop3](https://i.imgur.com/Iy4vvg2.png)

# Author
## Alan Nunes da Silva
### "Computer Enthusiast just for fun"
E-mail: [alann.625@gmail.com](mailto:alann.625@gmail.com)\
Linkedin: [Alan Nunes](https://www.linkedin.com/in/alan-nunes-848374152)

**Thank you, I hope you like it!**
