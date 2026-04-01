{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language": "python",
    "story": {
      "auth_token": "rV0Td2IVkmCHyCum-e3bMLk9FqDE5XJMzJRGETAKMhw=",
      "authorship_tag": "AB",
      "chapters": 66,
      "name": "Regular Expressions",
      "parser": {},
      "root": "https://github.com/habermanUIUC/CodeStories-lessons/blob/main/lessons/p4ds/upy/reg_ex1",
      "tag": "p4ds:upy:reg_ex1"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/cia161/colabs/blob/main/INFO407_RegEx_Part_1.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "#### **Introduction to Programming for Data Science using Python**\n",
        "\n",
        "#**Lesson: Regular Expressions - Part 1**"
      ],
      "metadata": {
        "id": "jNxwHPHIFC_W"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "###**Key Takeaways**\n",
        "\n",
        "\n",
        "* What is a regular expression\n",
        "\n",
        "\n",
        "* Why regular expressions are useful\n",
        "\n",
        "\n",
        "* How to create a regular expression in Python\n",
        "\n",
        "\n",
        "* What `findall` returns\n",
        "\n",
        "\n",
        "* What `.` , `*`, `\\s`, and `\\d` match\n",
        "\n",
        "\n",
        "* When to use the `[]` notation"
      ],
      "metadata": {
        "id": "2TtFpk-Nr2tZ"
      }
    },
    {
      "cell_type": "markdown",
      "source": [],
      "metadata": {
        "id": "8vvnXVTwae2Z"
      }
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "NdQ9MhHCPS2Z"
      },
      "source": [
        "Grab yourself a warm drink and settle in; this lesson's a bit longer than most. If you don't have the time to work through it slowly, reschedule a better time to do this lesson. If there's one thing that will help you parse and wrangle data the most, it's regular expressions.\n",
        "\n",
        "We have seen some methods (functions attached to objects) on the string data type that provided some very handy capabilities. For example, `split()` transforms a string into a list of tokens. Similarly `strip()` and `replace()` give an easy way to remove or replace unwanted values. The string has so many useful features that it's always worth re-visiting its [documentation](https://docs.python.org/3.6/library/stdtypes.html#string-methods).\n",
        "\n",
        "However, even with mastery of all those methods, there are some things that would be extremely tedious if that's all we had to work with. Let's take a look at some examples.\n",
        "\n",
        "![Frankenstein Cover](https://www.gutenberg.org/cache/epub/84/pg84.cover.medium.jpg)\n",
        "#**Words from Frankenstein**\n",
        "We will use the text from \"Frankenstein; Or, The Modern Prometheus\" by Mary Wollstonecraft Shelley (found on [Project Gutenberg](https://www.gutenberg.org/ebooks/84)). The file you need to download and use here is available on [Github](https://github.com/Xyzic/INFO407/blob/main/Resources/Text%20Files/clean_frankenstein.txt).\n",
        "\n",
        "Let's get the text into our notebook. We will use this text throughout the lesson. If your notebook gets disconnected, you should upload clean_frankenstein.txt file and then run this cell before continuing:\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "eQHDaFzOPS2c",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "b9275095-fdcf-4d80-f279-7f2fef729d69"
      },
      "source": [
        "# You should upload the clean_frankenstein.txt file to Colab locally before running this cell\n",
        "\n",
        "def read_frankenstein():\n",
        "  with open('clean_frankenstein.txt', 'r') as fd:\n",
        "    txt = fd.read()\n",
        "  return txt\n",
        "\n",
        "BOOK_TEXT = read_frankenstein() # You will use this to test your code through the lesson\n",
        "\n",
        "# Here we are extracting only first chapter of the book!\n",
        "book_idx = BOOK_TEXT.find(\"Letter 1\\n\\n\")\n",
        "idx = BOOK_TEXT.find(\"Letter 2\\n\\n\")\n",
        "CHAPTER_ONE = BOOK_TEXT[book_idx:idx].strip()\n",
        "\n",
        "print(CHAPTER_ONE[0:365])"
      ],
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Letter 1\n",
            "\n",
            "_To Mrs. Saville, England._\n",
            "\n",
            "\n",
            "St. Petersburgh, Dec. 11th, 17—.\n",
            "\n",
            "\n",
            "You will rejoice to hear that no disaster has accompanied the\n",
            "commencement of an enterprise which you have regarded with such evil\n",
            "forebodings. I arrived here yesterday, and my first task is to assure\n",
            "my dear sister of my welfare and increasing confidence in the success\n",
            "of my undertaking.\n",
            "\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "###**Finding Words**\n",
        "When doing text analysis, the first task is to figure out how to get all the words from a passage of text.\n",
        "\n",
        "Let's take a quick look at how using string's `split()` method to get all the \"words\" of a book falls short."
      ],
      "metadata": {
        "id": "e0xdZglFQBYX"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "YU0JCglyPS2i",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "ffe10ec5-6034-4f65-8422-54a48df65f33"
      },
      "source": [
        "def find_words(text):\n",
        "    words = text.split()\n",
        "    uniq  = sorted(set(words))\n",
        "    print(len(uniq))\n",
        "\n",
        "find_words(BOOK_TEXT)"
      ],
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "11607\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "\n",
        "We get 11,608 'words'. However, in this set, words with different case (You and you) will be considered different words. We can fix this quickly:"
      ],
      "metadata": {
        "id": "hbZsbNLGQLLr"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "qqkKoeB_PS3V",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "203b5ab2-86fa-4eeb-97aa-ef7e7f2b5d56"
      },
      "source": [
        "def get_uniq_words(text):\n",
        "    words = text.split()\n",
        "    words  = sorted(words)\n",
        "    uniq = set([x.lower() for x in words])\n",
        "    return uniq\n",
        "\n",
        "print(len(get_uniq_words(BOOK_TEXT)))"
      ],
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "11228\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "With this improvement, we get 11,229 words. However if you inspect the contents of uniq (e.g `list(uniq)[0:20])` words, we see a few issues:\n",
        "\n",
        "* words have punctuation in them\n",
        "* phrases like `Wait—wait!`(those without spaces) are treated as a single word\n",
        "\n",
        "If we pre-clean the text, i.e. before we `split()`, by removing all punctuation except the single quote (so we don't split contractions -- e.g. `ain‘t`), we end up with a different number of unique tokens and all tokens after case normalization. However, that punctuation may be valuable in our analysis as well."
      ],
      "metadata": {
        "id": "ZYrWZoB7QP9O"
      }
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "5GA3UjDVPS3b"
      },
      "source": [
        "#**Entering Regular Expressions**\n",
        "As we have just seen, we need to do a double pass over the tokens, once to remove unwanted punctuation and another to split the text based on whitespace, i.e. `str.split()`. Although efficiency isn't always a goal, it becomes necessary as the datasets grow. However, the goal in this lesson is to see if we can do this by describing what we want to extract from the text, rather than writing a lot of code to do it.\n",
        "\n",
        "The \"tool\" we are about to introduce, *regular expressions*, provides a language to make it 'easy' to extract patterns from text. You don't need to use them, but they become very handy to express what you want to extract, rather than writing the code to tell the computer how to do it. This is essentially the difference between imperative languages (like Python) and declarative languages (like SQL). Although calling regular expressions a declarative language is a bit of a stretch. The regular expression capability is provided by the re module. You must include that module at the top of your Python code to use regular expressions:\n",
        "\n",
        "```\n",
        "import re\n",
        "```\n",
        "\n",
        "If the only thing you were interested in is tokenizing the text, then `split()` would be fine. But we want the words. Of course we have to define what it means to be a word. Let's say that a word is any *token* (a group of 1 or more characters) that contains at least one letter. With regular expressions, we can capture that expression using a pattern. Using regular expressions is usually three basic steps:"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# type the code here\n",
        "import re\n"
      ],
      "metadata": {
        "id": "mUAzMvD7RLpW"
      },
      "execution_count": 6,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "### **1. Define the pattern:**\n",
        "```\n",
        "pattern = '[A-Za-z]+'\n",
        "```\n",
        "Notice that:\n",
        "* The pattern is always a string (hence, you need the quotes)\n",
        "* In this case, we put what we are looking for inside `[]` brackets. These brackets hold groups of characters (called a character set or *character class*). So `[A-Z]` means ***match*** any uppercase letter (`[a-z]` matches any lowercase letter).\n",
        "* The `+` means 1 or more of the previous pattern or the thing to its left (in this case the stuff inside the brackets).\n",
        "* The bracket matches *unordered* characters -- regardless of the order of the characters inside the brackets.\n",
        "\n",
        "We would describe this pattern as \"one or more characters that are either upper or lower case letters\".\n",
        "\n",
        "\n",
        "The defined pattern would attempt to find any token that consists of all letters and any non letter (something that is **not** `A-Za-z`) would serve as a split or demarcation point."
      ],
      "metadata": {
        "id": "zHiwiXS6Q_sP"
      }
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "N6vVF6NfFSgG"
      },
      "execution_count": 6,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# type the code here\n",
        "\n"
      ],
      "metadata": {
        "id": "RWSBHD3QTwMn"
      },
      "execution_count": 7,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "gfLumyJ0FSS0"
      },
      "execution_count": 7,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "### **2. Compile the pattern**\n",
        "Use the `re.compile()` method to compile the pattern:\n",
        "```\n",
        " pattern = '[A-Za-z]+'\n",
        " regex   = re.compile(pattern)\n",
        "```\n",
        "\n",
        "This creates a regular expression object that you can use to call different methods on. In this lesson we will only be looking at the regular expression `findall` method. The pattern is used to determine what to look for in a body of text.\n"
      ],
      "metadata": {
        "id": "mKD7XcqkRGjj"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# type the example\n"
      ],
      "metadata": {
        "id": "q27y8IP-UP81"
      },
      "execution_count": 8,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "### **3. Use the compiled pattern**\n",
        "Use the `findall()` method on the object returned by `compile`. It's a regular expression object:\n",
        "\n",
        "```\n",
        "import re\n",
        "\n",
        "def regex_find_words_demo(text):\n",
        "  pattern = '[A-Za-z]+'          # 1 create a pattern\n",
        "  regex   = re.compile(pattern)  # 2 compile it\n",
        "  return regex.findall(text)     # 3 return those tokens that match the pattern\n",
        "\n",
        "a = regex_find_words_demo(BOOK_TEXT)\n",
        "print(len(a))\n",
        "```\n",
        "Be sure to type and run this code (you should see 75,310)"
      ],
      "metadata": {
        "id": "ZR8hKwTHRJH6"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "jTw-J3a6PS3d",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "9b654472-30e6-4618-a6f3-ff394f4c1b46"
      },
      "source": [
        "# Type the above example here\n",
        "import re\n",
        "\n",
        "def regex_find_words_demo(text):\n",
        "  pattern = '[A-Za-z]+'          # 1 create a pattern\n",
        "  regex   = re.compile(pattern)  # 2 compile it\n",
        "  return regex.findall(text)     # 3 return those tokens that match the pattern\n",
        "\n",
        "a = regex_find_words_demo(BOOK_TEXT)\n",
        "print(len(a))"
      ],
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "75310\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "> ***Coder's Log:*** This is indeed another lesson that if you don't run each sample code and move to the next one without understanding what you just ran, it will be impossible to learn the nuances being taught.\n",
        "\n",
        "One small fix we need to do. The pattern finds words regardless of the case (it is letter-case insensitive). So `findall()` will return the words in their original case (it does NOT transform text). We need to be sure words like 'You' and 'you' are treated as the same word.\n",
        "\n",
        "The normalization step is still needed with regular expressions. Let's fix that.\n",
        "\n",
        "Type in the following (either using a new code cell or a previous one). When you run it, you should get 6,980 'words' -- any token that consists of all letters.\n",
        "\n",
        "```\n",
        "def get_uniq_wordset(words):\n",
        "  return set([x.lower() for x in words])\n",
        "\n",
        "a = get_uniq_wordset(regex_find_words_demo(BOOK_TEXT))\n",
        "print(len(a))\n",
        "```"
      ],
      "metadata": {
        "id": "KikbekEtS1s_"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Type the code here"
      ],
      "metadata": {
        "id": "bl7EAEyB62Bq"
      },
      "execution_count": 10,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def get_uniq_wordset(words):\n",
        "  return set([x.lower() for x in words])\n",
        "\n",
        "a = get_uniq_wordset(regex_find_words_demo(BOOK_TEXT))\n",
        "print(len(a))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "AlMbaWSoGGWX",
        "outputId": "02787693-fe7e-4574-a6c3-ab3130565d5a"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "6980\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Let's start adjusting the pattern to see how the number of words changes as we change the pattern. We will create a new function where we can pass in the pattern for the regular expression engine to use:"
      ],
      "metadata": {
        "id": "zN0luCfQRKnu"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "GrzTeCZiPS3e",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "d0a790f3-2131-4257-eeb9-14384165643e"
      },
      "source": [
        "import re\n",
        "def regex_find_words(text, pattern):\n",
        "  regex = re.compile(pattern)  # Compile it\n",
        "  return regex.findall(text)   # Return those tokens that match the pattern\n",
        "\n",
        "pattern = '[A-Za-z]+'\n",
        "print(len(regex_find_words(BOOK_TEXT, pattern)))"
      ],
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "75310\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Now let's consider keeping tokens that have numbers in them (e.g. 1st) or those that are all numbers (e.g. 10 cents). We can extend our pattern to include numbers (we use the character class 0-9)."
      ],
      "metadata": {
        "id": "qjyZazNJUPZo"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "pw9Eq8tiPS3v",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "3665628e-1511-4e1b-a44d-083adc822ced"
      },
      "source": [
        "def pattern_demo():\n",
        "    pattern = '[0-9A-Za-z]+'\n",
        "    words = regex_find_words(BOOK_TEXT, pattern)\n",
        "    uniq = get_uniq_wordset(words)\n",
        "\n",
        "    print(len(words))\n",
        "    print(len(uniq))\n",
        "\n",
        "pattern_demo()"
      ],
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "75348\n",
            "7016\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Now the total is 7,016 unique tokens. Can you use the set data type and the difference method to find what numbers are captured now with this new pattern?\n",
        "\n",
        "###**Getting Closer**\n",
        "So the question is why is this NOT the same value that we would get using `split()`? The issue is that with the regular expressions we didn't capture any punctuation including the single quote. So we need to add that in:\n",
        "```\n",
        "pattern = '[’0-9A-Za-z]+'\n",
        "```\n",
        "Since the apostrophe character used in the book (`’`)is different than the single quotes used to wrap a pattern (`'`), this string will be interpreted correctly. However, if the book required you to use the same character, you would need to escape the single quote you want to find, i.e. `\\’`. Alternatively, you could use double quotes:\n",
        "```\n",
        "pattern = \"[’0-9A-Za-z]+\"\n",
        "```\n",
        "Once you run that pattern. You get 7,062 unique matches!"
      ],
      "metadata": {
        "id": "ROT0yB1lUq13"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# type here the demo with the new pattern\n",
        "def pattern_demo():\n",
        "    pattern = \"[’0-9A-Za-z]+\"\n",
        "    words = regex_find_words(BOOK_TEXT, pattern)\n",
        "    uniq = (get_uniq_wordset(words))\n",
        "    print(len(uniq))\n",
        "    print(sorted(list(uniq)))\n",
        "\n",
        "\n",
        "pattern_demo()"
      ],
      "metadata": {
        "id": "Gz0PMVxpZ-oP",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "01b20fbd-6282-4d24-87d0-927fccd0447c"
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "7062\n",
            "['1', '10', '11', '11th', '12', '12th', '13', '13th', '14', '15', '16', '17', '18', '18th', '19', '19th', '2', '20', '21', '22', '23', '24', '26th', '27th', '28th', '2d', '3', '31st', '4', '5', '5th', '6', '7', '7th', '8', '9', '9th', 'a', 'abandon', 'abandoned', 'abbey', 'abhor', 'abhorred', 'abhorrence', 'abhorrent', 'ability', 'abject', 'able', 'aboard', 'abode', 'abortion', 'abortive', 'about', 'above', 'abroad', 'abrupt', 'absence', 'absent', 'absolute', 'absolutely', 'absolution', 'absorbed', 'absorbing', 'abstained', 'abstruse', 'abyss', 'acceded', 'accent', 'accents', 'accept', 'acceptance', 'access', 'accident', 'accidentally', 'accidents', 'accompanied', 'accompany', 'accomplish', 'accomplished', 'accomplishment', 'accomplishments', 'accorded', 'according', 'accordingly', 'account', 'accounted', 'accounts', 'accumulated', 'accumulation', 'accuracy', 'accurate', 'accursed', 'accusation', 'accusations', 'accuse', 'accused', 'accuses', 'accustomed', 'achieve', 'achieved', 'achievements', 'aching', 'acknowledged', 'acme', 'acorns', 'acquaintance', 'acquaintances', 'acquainted', 'acquiesced', 'acquire', 'acquired', 'acquirement', 'acquiring', 'acquisition', 'acquit', 'acquittal', 'acquitted', 'across', 'act', 'acted', 'acting', 'action', 'actions', 'active', 'activity', 'actor', 'acts', 'actual', 'actually', 'actuated', 'acuteness', 'adam', 'adam’s', 'adapt', 'add', 'added', 'additional', 'address', 'addressed', 'adduced', 'adequate', 'adieu', 'adjacent', 'adjuration', 'admirable', 'admiration', 'admire', 'admired', 'admission', 'admit', 'admittance', 'adopted', 'adoration', 'adored', 'adorned', 'adorns', 'adrift', 'advance', 'advanced', 'advancement', 'advancing', 'advantage', 'advantages', 'adventure', 'adventurer', 'adventurous', 'adversary', 'adversary’s', 'adversity', 'advice', 'advise', 'advocate', 'aerial', 'affability', 'affair', 'affairs', 'affectation', 'affected', 'affecting', 'affection', 'affectionate', 'affectionately', 'affections', 'affirm', 'affirmative', 'afflicted', 'affluence', 'afford', 'afforded', 'affording', 'affords', 'affright', 'afraid', 'africa', 'after', 'afternoon', 'afterwards', 'again', 'against', 'agatha', 'age', 'aged', 'agents', 'ages', 'aggravation', 'agile', 'agitated', 'agitates', 'agitation', 'ago', 'agonies', 'agonised', 'agonising', 'agony', 'agree', 'agreeable', 'agreed', 'agrippa', 'ah', 'aid', 'aided', 'aiguilles', 'aim', 'aimed', 'air', 'airs', 'airy', 'akin', 'alarm', 'alarmed', 'alarming', 'alas', 'albatross', 'albertus', 'alchemists', 'alighted', 'alighting', 'alike', 'alive', 'all', 'alleged', 'alleging', 'alleviate', 'alleviated', 'allied', 'allotted', 'allow', 'allowed', 'allowing', 'alloy', 'allude', 'alluded', 'allured', 'allurements', 'alluring', 'allusion', 'almighty', 'almost', 'alone', 'along', 'aloud', 'alphonse', 'alpine', 'alps', 'already', 'also', 'alter', 'alteration', 'alterations', 'altered', 'alternate', 'although', 'altogether', 'always', 'am', 'amassed', 'amazed', 'amazing', 'ambition', 'ameliorate', 'amend', 'america', 'american', 'amiable', 'amid', 'amidst', 'among', 'amongst', 'amounted', 'amphitheatre', 'ample', 'amuse', 'amused', 'amusement', 'amusements', 'an', 'analysing', 'analysis', 'anatomise', 'anatomy', 'ancestors', 'anchor', 'ancient', 'and', 'andes', 'andrew’s', 'anew', 'angel', 'angelic', 'angelica', 'angel’s', 'anger', 'angrily', 'angry', 'anguish', 'animal', 'animals', 'animate', 'animated', 'animating', 'animation', 'annihilation', 'announce', 'announced', 'annoyed', 'annoying', 'anon', 'another', 'another’s', 'answer', 'answered', 'answers', 'antelope', 'anticipated', 'anticipation', 'anticipations', 'antipathy', 'antique', 'antiquity', 'anxiety', 'anxious', 'anxiously', 'any', 'anyone', 'anything', 'apart', 'apartment', 'apartments', 'apathy', 'apothecary', 'appalling', 'apparatus', 'apparel', 'apparent', 'apparently', 'apparition', 'appeal', 'appeals', 'appear', 'appearance', 'appearances', 'appeared', 'appearing', 'appears', 'appeased', 'appertaining', 'appetite', 'apple', 'application', 'applied', 'apply', 'appointment', 'appreciate', 'apprehended', 'apprehending', 'apprehension', 'apprehensions', 'approach', 'approached', 'approaching', 'approbation', 'appropriated', 'approve', 'approved', 'apt', 'arab', 'arabian', 'arabic', 'arbiters', 'arch', 'archangel', 'ardent', 'ardently', 'ardour', 'arduous', 'are', 'argue', 'argument', 'arguments', 'aright', 'ariosto', 'arise', 'arisen', 'arising', 'arm', 'armada', 'armed', 'arms', 'arose', 'around', 'aroused', 'arrange', 'arranged', 'arrangements', 'arranging', 'arrest', 'arrested', 'arrival', 'arrive', 'arrived', 'arrives', 'arriving', 'arrow', 'arrowy', 'art', 'arteries', 'artery', 'arthur', 'arthur’s', 'article', 'articles', 'articulate', 'artifice', 'artist', 'arts', 'arve', 'arveiron', 'as', 'ascend', 'ascended', 'ascent', 'ascertain', 'ascertaining', 'ascribed', 'ashamed', 'ashes', 'asia', 'asiatics', 'aside', 'ask', 'asked', 'asks', 'asleep', 'aspect', 'aspirations', 'aspire', 'aspired', 'aspires', 'ass', 'assailed', 'assassin', 'assassinated', 'assemblage', 'assemblages', 'assemblance', 'assembled', 'asserted', 'assertion', 'asseverations', 'assigned', 'assist', 'assistance', 'assistants', 'assisted', 'assisting', 'assizes', 'associate', 'associated', 'associates', 'association', 'assuage', 'assume', 'assumed', 'assurance', 'assurances', 'assure', 'assured', 'assuredly', 'assures', 'astonished', 'astonishing', 'astonishment', 'astounded', 'astounding', 'asylum', 'at', 'ate', 'atlantic', 'atmosphere', 'atone', 'atrocious', 'attach', 'attached', 'attachment', 'attack', 'attacked', 'attacks', 'attain', 'attained', 'attainment', 'attempt', 'attempted', 'attempts', 'attend', 'attendance', 'attendant', 'attendants', 'attended', 'attending', 'attends', 'attention', 'attentions', 'attentive', 'attentively', 'attest', 'attitude', 'attract', 'attracted', 'attractions', 'attractive', 'attracts', 'attributed', 'audible', 'audibly', 'auditor', 'aught', 'augmented', 'augmenting', 'auguries', 'augury', 'august', 'aunt', 'austria', 'austrian', 'author', 'authority', 'authors', 'autumn', 'avail', 'availed', 'avalanche', 'avenge', 'avenue', 'averred', 'averse', 'aversion', 'avert', 'avidity', 'avoid', 'avoided', 'avow', 'avowal', 'avowed', 'await', 'awaiting', 'awake', 'awaken', 'awakened', 'awaking', 'award', 'aware', 'away', 'awe', 'awful', 'awoke', 'ay', 'babe', 'babes', 'back', 'backs', 'bad', 'bade', 'baffled', 'balanced', 'balancing', 'ball', 'ballots', 'balminess', 'balmy', 'ban', 'banish', 'banished', 'banker', 'banks', 'barbarity', 'barbarous', 'barbarously', 'bare', 'bared', 'barks', 'barn', 'barred', 'barren', 'barricade', 'barrier', 'barriers', 'base', 'basest', 'basket', 'bat', 'bathed', 'baths', 'bauble', 'be', 'beach', 'beam', 'beaming', 'bear', 'bearing', 'bears', 'beast', 'beasts', 'beat', 'beaten', 'beaufort', 'beaufort’s', 'beauties', 'beautiful', 'beauty', 'became', 'because', 'become', 'becomes', 'becoming', 'bed', 'bedewed', 'bedim', 'bedroom', 'beds', 'bedside', 'been', 'befall', 'befallen', 'befitting', 'before', 'beg', 'began', 'beggar', 'beggars', 'begged', 'begin', 'beginning', 'begins', 'begone', 'begun', 'behalf', 'behaviour', 'beheld', 'behind', 'behold', 'beholding', 'being', 'beings', 'belief', 'believe', 'believed', 'believes', 'believing', 'belong', 'belonged', 'belonging', 'belongs', 'beloved', 'below', 'belrive', 'bend', 'bending', 'beneath', 'benefactor', 'benefactors', 'beneficence', 'beneficial', 'benefit', 'benefits', 'benevolence', 'benevolent', 'benevolently', 'benignity', 'bent', 'benumbed', 'bernard’s', 'berries', 'beside', 'besides', 'besieged', 'besought', 'bespoke', 'best', 'bestow', 'bestowed', 'bestowing', 'betook', 'betray', 'betrayed', 'better', 'between', 'beware', 'bewildered', 'beyond', 'bid', 'bidding', 'bids', 'bier', 'bill', 'bind', 'binding', 'bird', 'birds', 'biron', 'birth', 'bitter', 'bitterest', 'bitterly', 'bitterness', 'black', 'blackbird', 'blackest', 'blackness', 'blamable', 'blame', 'blameless', 'blanc', 'blankets', 'blast', 'blasted', 'bleak', 'bleakness', 'bless', 'blessed', 'blessing', 'blessings', 'blew', 'blight', 'blind', 'blinded', 'blindness', 'bliss', 'blood', 'bloodless', 'bloodshed', 'bloody', 'bloom', 'bloomed', 'blooming', 'blossom', 'blot', 'blotted', 'blow', 'blows', 'blue', 'blunt', 'board', 'boarder', 'boast', 'boat', 'boats', 'bodies', 'bodily', 'body', 'boils', 'bold', 'bolt', 'bolts', 'bondage', 'bonds', 'bone', 'bones', 'book', 'books', 'bore', 'born', 'borne', 'bosom', 'bosoms', 'both', 'bottom', 'bought', 'bound', 'boundaries', 'boundary', 'bounded', 'bounding', 'boundless', 'bounds', 'bounty', 'bourne', 'bowing', 'boy', 'boyhood', 'boy’s', 'braces', 'braided', 'brain', 'brake', 'brambles', 'branch', 'branches', 'brand', 'brandy', 'brave', 'brawling', 'bread', 'break', 'breakers', 'breakfast', 'breaking', 'breast', 'breath', 'breathe', 'breathed', 'breathless', 'bred', 'breeze', 'breezes', 'brethren', 'bridal', 'bride', 'brides', 'bridge', 'briefly', 'bright', 'brightest', 'brightly', 'brightness', 'brilliant', 'bring', 'bringing', 'brink', 'britain', 'broad', 'broke', 'broken', 'brooded', 'brooding', 'brook', 'brother', 'brotherly', 'brothers', 'brother’s', 'brought', 'brow', 'brows', 'bruised', 'brutality', 'brute', 'bud', 'budding', 'buds', 'buffeted', 'building', 'buildings', 'built', 'burden', 'burdened', 'buried', 'burn', 'burned', 'burning', 'burns', 'burnt', 'burst', 'bursting', 'bury', 'bushes', 'busied', 'busier', 'busily', 'business', 'bustle', 'busy', 'but', 'buy', 'by', 'c', 'cabin', 'cabinets', 'cabriolet', 'cadence', 'cake', 'calamities', 'calamity', 'calculated', 'calculating', 'calculations', 'call', 'called', 'calling', 'callous', 'calm', 'calmed', 'calmer', 'calmly', 'calmness', 'came', 'campagne', 'can', 'candle', 'candour', 'cannot', 'canopied', 'canopy', 'canst', 'canvassed', 'capable', 'capacious', 'capacities', 'capacity', 'cape', 'capitulated', 'caprice', 'caprices', 'captain', 'captive', 'care', 'career', 'carefully', 'careless', 'carelessly', 'carelessness', 'cares', 'caresses', 'carnage', 'caroline', 'carpeted', 'carriage', 'carriages', 'carried', 'carry', 'carrying', 'case', 'casement', 'cast', 'casting', 'castle', 'castles', 'casualties', 'catalogue', 'cataract', 'catastrophe', 'catching', 'catholic', 'caught', 'causation', 'cause', 'caused', 'causes', 'causing', 'caution', 'cave', 'caves', 'cease', 'ceased', 'ceasing', 'celebrated', 'celestial', 'cell', 'cemetery', 'cenis', 'centre', 'centred', 'century', 'ceremony', 'certain', 'certainly', 'certainty', 'ch', 'chain', 'chained', 'chains', 'chair', 'chairs', 'chaise', 'chamber', 'chamois', 'chamounix', 'chance', 'chanced', 'chances', 'change', 'changeable', 'changed', 'changes', 'changing', 'channel', 'chapter', 'character', 'characterise', 'characteristically', 'characters', 'charge', 'charged', 'charging', 'charity', 'charles', 'charm', 'charmed', 'charming', 'charms', 'charnel', 'chase', 'chasms', 'chastened', 'chastise', 'chattered', 'cheat', 'check', 'checked', 'cheek', 'cheeks', 'cheered', 'cheerful', 'cheerfully', 'cheerfulness', 'cheering', 'cheese', 'chemical', 'chemist', 'chemistry', 'chemists', 'cherish', 'cherished', 'cherub', 'chief', 'chiefly', 'child', 'childhood', 'childish', 'childless', 'children', 'child’s', 'chill', 'chilled', 'chilly', 'chimera', 'chimeras', 'chimerical', 'chimney', 'chink', 'chinks', 'chivalrous', 'chivalry', 'choice', 'choicest', 'choked', 'choose', 'chord', 'chosen', 'christian', 'christianity', 'church', 'churchyard', 'circle', 'circulates', 'circumstance', 'circumstances', 'circumstantial', 'citadel', 'city', 'civilised', 'clad', 'claim', 'claimed', 'claims', 'clapped', 'clapping', 'clasp', 'clasped', 'clasping', 'class', 'classes', 'classifications', 'clay', 'clean', 'cleaning', 'clear', 'cleared', 'clearly', 'clearness', 'clemency', 'clerval', 'clever', 'cliffs', 'climate', 'climbing', 'climes', 'cling', 'clinging', 'clings', 'cloak', 'clock', 'close', 'closed', 'closely', 'closer', 'closest', 'closing', 'clothed', 'clothes', 'clothing', 'cloud', 'clouded', 'cloudless', 'clouds', 'cloudy', 'clue', 'clump', 'clung', 'coach', 'coarse', 'coarser', 'coarsest', 'coast', 'coasting', 'code', 'coffin', 'coincidences', 'cold', 'coldness', 'coleridge’s', 'colleague', 'collect', 'collected', 'collecting', 'collections', 'college', 'colleges', 'cologne', 'colonization', 'colour', 'colours', 'combat', 'combined', 'combustibles', 'come', 'comes', 'comfort', 'comfortable', 'comforter', 'comfortless', 'coming', 'command', 'commanded', 'commence', 'commenced', 'commencement', 'commences', 'comment', 'commerce', 'commiserate', 'commission', 'commit', 'committed', 'committing', 'common', 'communicate', 'communicated', 'communicating', 'communication', 'communion', 'community', 'como', 'compact', 'companion', 'companions', 'companionship', 'company', 'comparable', 'comparative', 'compared', 'compass', 'compassed', 'compassion', 'compassionate', 'compassionated', 'compensate', 'compensated', 'competent', 'complacency', 'complain', 'complained', 'complaints', 'complete', 'completed', 'completely', 'completes', 'completion', 'complex', 'complexion', 'complexions', 'complexity', 'complied', 'comply', 'compose', 'composed', 'composes', 'composing', 'composure', 'comprehend', 'comprehended', 'comprehensive', 'comprised', 'comrades', 'conceal', 'concealed', 'concealing', 'concealment', 'concede', 'conceited', 'conceive', 'conceived', 'conceiving', 'concentrated', 'conception', 'concern', 'concerned', 'concerning', 'concert', 'conciliating', 'conclude', 'concluded', 'conclusion', 'conclusions', 'concussion', 'condemn', 'condemnation', 'condemned', 'condemns', 'condescension', 'condition', 'conditions', 'conduce', 'conducive', 'conduct', 'conducted', 'conducting', 'conductor', 'conductors', 'confer', 'confess', 'confessed', 'confessing', 'confession', 'confessor', 'confide', 'confided', 'confidence', 'confident', 'confidential', 'confine', 'confined', 'confinement', 'confines', 'confirm', 'confirmation', 'confirmed', 'confirms', 'confiscated', 'conflagration', 'conflict', 'conflicting', 'conformation', 'confused', 'confusedly', 'confusion', 'congeal', 'congenial', 'congratulatory', 'congregated', 'conjecture', 'conjectured', 'conjectures', 'conjure', 'conjured', 'connected', 'connection', 'conquer', 'conquered', 'conscience', 'conscious', 'consciousness', 'consecrate', 'consecrated', 'consent', 'consented', 'consequence', 'consequences', 'consequently', 'consider', 'considerable', 'considerably', 'considerate', 'considerateness', 'consideration', 'considerations', 'considered', 'considering', 'consist', 'consisted', 'consistent', 'consolation', 'console', 'consoled', 'consoles', 'constant', 'constantinople', 'constantly', 'consternation', 'constrained', 'construct', 'constructed', 'construed', 'consulted', 'consume', 'consumed', 'consumes', 'consummate', 'consummated', 'consummation', 'consumption', 'contain', 'contained', 'containing', 'contemplate', 'contemplated', 'contemplation', 'contempt', 'content', 'contented', 'contention', 'contentment', 'contents', 'contest', 'continual', 'continually', 'continuation', 'continue', 'continued', 'continuing', 'contortions', 'contradictory', 'contrary', 'contrast', 'contributed', 'contributes', 'contrived', 'control', 'contumely', 'convalescence', 'convenience', 'conveniently', 'convent', 'conversation', 'conversations', 'converse', 'conversed', 'conversing', 'convey', 'conveyed', 'conveys', 'convict', 'convicted', 'conviction', 'convinced', 'convulsed', 'convulsions', 'convulsive', 'cooking', 'cool', 'coolness', 'cooped', 'cop', 'cope', 'copies', 'cord', 'cordial', 'core', 'cornelius', 'corner', 'corpse', 'corrected', 'correspondence', 'corruption', 'cot', 'cottage', 'cottager', 'cottagers', 'cottages', 'could', 'counsel', 'counsellors', 'countenance', 'countenances', 'countless', 'countries', 'country', 'countryman', 'countrymen', 'coupar', 'courage', 'courageous', 'course', 'courses', 'court', 'courtyard', 'cousin', 'cousins', 'covered', 'covers', 'coveted', 'cow', 'coward', 'cowardice', 'cowards', 'cows', 'cracked', 'cracking', 'crags', 'cramped', 'crash', 'craving', 'crawled', 'crawling', 'creaking', 'create', 'created', 'creates', 'creating', 'creation', 'creations', 'creator', 'creators', 'creature', 'creatures', 'creature’s', 'credit', 'credited', 'creek', 'crept', 'crevice', 'crevices', 'crew', 'cried', 'cries', 'crime', 'crimes', 'criminal', 'criminality', 'critical', 'croaking', 'cross', 'crossed', 'crossing', 'crowd', 'crowded', 'crowding', 'crown', 'crucible', 'cruel', 'cruellest', 'cruelly', 'cruelty', 'crush', 'crushed', 'cry', 'culled', 'cultivated', 'cultivating', 'cultivation', 'cumberland', 'cup', 'curbed', 'curdles', 'cure', 'curiosities', 'curiosity', 'curious', 'curiously', 'curling', 'current', 'curse', 'cursed', 'curses', 'cursory', 'curtain', 'custom', 'customs', 'cut', 'cypress', 'd', 'dabble', 'dabbled', 'dagger', 'daily', 'damp', 'damps', 'danced', 'dancing', 'danger', 'dangerous', 'dangerously', 'dangers', 'daniel', 'dank', 'dante', 'dare', 'dared', 'daring', 'dark', 'darkened', 'darkness', 'darling', 'darted', 'dash', 'dashed', 'dashing', 'date', 'dated', 'dates', 'daughter', 'daughter’s', 'dauntless', 'dawn', 'dawned', 'day', 'daybreak', 'daydreams', 'daylight', 'days', 'days’', 'day’s', 'dazzled', 'dazzling', 'de', 'dead', 'deadly', 'deal', 'dealing', 'dear', 'dearer', 'dearest', 'dearly', 'death', 'deathbed', 'deathlike', 'deaths', 'debar', 'debarred', 'debasing', 'debilitated', 'debility', 'debts', 'dec', 'decay', 'decayed', 'decaying', 'deceit', 'deceived', 'december', 'decide', 'decided', 'decidedly', 'decides', 'decipher', 'decision', 'decisive', 'deck', 'declamatory', 'declaration', 'declare', 'declared', 'decline', 'declined', 'declining', 'decorations', 'decreased', 'decreasing', 'decreed', 'dedicate', 'dedicated', 'deduce', 'deduced', 'deed', 'deeds', 'deem', 'deemed', 'deep', 'deeper', 'deepest', 'deeply', 'deer', 'defeat', 'defects', 'defence', 'defend', 'deference', 'deferred', 'defiance', 'define', 'deformed', 'deformity', 'degenerating', 'degradation', 'degraded', 'degree', 'degrees', 'dejected', 'dejection', 'delay', 'delayed', 'delicacy', 'delicate', 'delicious', 'delight', 'delighted', 'delightful', 'delights', 'delineate', 'delirium', 'deliver', 'delivered', 'deliverer', 'delusion', 'demand', 'demanded', 'demands', 'demeanour', 'demoniacal', 'demonstrate', 'denial', 'denied', 'denote', 'denounce', 'dens', 'dense', 'deny', 'depart', 'departed', 'department', 'departure', 'depend', 'depended', 'dependent', 'depending', 'deplored', 'deposed', 'deposited', 'depositing', 'deposition', 'depraved', 'depravity', 'deprecate', 'depressed', 'deprived', 'deprives', 'depth', 'depths', 'deputation', 'derange', 'deranged', 'derby', 'derive', 'derives', 'descend', 'descended', 'descending', 'descends', 'descent', 'describe', 'described', 'description', 'desert', 'deserted', 'desertion', 'deserts', 'deserve', 'deserved', 'deserving', 'design', 'designed', 'designs', 'desire', 'desired', 'desires', 'desiring', 'desirous', 'desolate', 'desolated', 'desolating', 'desolation', 'despair', 'despaired', 'despairing', 'desperate', 'desperately', 'desperation', 'despicable', 'despise', 'despised', 'despite', 'despond', 'despondence', 'despondency', 'despondent', 'desponding', 'destination', 'destined', 'destiny', 'destitute', 'destroy', 'destroyed', 'destroyer', 'destroying', 'destruction', 'destructive', 'detail', 'details', 'detain', 'detect', 'determination', 'determined', 'determining', 'detest', 'detestable', 'detestation', 'detested', 'detracts', 'detrimental', 'developed', 'development', 'deviating', 'devices', 'devil', 'devilish', 'devils', 'devolved', 'devote', 'devoted', 'devoting', 'devotion', 'devoured', 'devouring', 'dew', 'dews', 'diabolical', 'diabolically', 'dialects', 'dialogue', 'dictate', 'dictated', 'did', 'didst', 'die', 'died', 'diet', 'differed', 'difference', 'different', 'differing', 'difficult', 'difficulties', 'difficulty', 'diffidence', 'diffident', 'diffused', 'diffusing', 'digging', 'dignity', 'dilatoriness', 'dilatory', 'diligence', 'diligences', 'dim', 'dimmed', 'dimming', 'dimples', 'dinner', 'dire', 'direct', 'directed', 'direction', 'directions', 'directly', 'dirge', 'dirt', 'disappeared', 'disappointed', 'disappointment', 'disappointments', 'disaster', 'disasters', 'disastrous', 'disbelief', 'discerned', 'discerning', 'discernment', 'discharge', 'disciple', 'discipline', 'disclose', 'disclosed', 'discompose', 'disconcerted', 'disconsolate', 'discontent', 'discontented', 'discourse', 'discover', 'discovered', 'discoverers', 'discoveries', 'discovering', 'discovery', 'discrimination', 'disdain', 'disease', 'disencumbered', 'disgrace', 'disguise', 'disgust', 'disgusted', 'disgusting', 'disinclined', 'disinterested', 'disk', 'dislike', 'disliked', 'dismal', 'dismally', 'dismay', 'dismissed', 'dismissing', 'dismount', 'disobey', 'disorder', 'disowned', 'dispatched', 'dispel', 'dispelled', 'dispelling', 'dispersed', 'displayed', 'displaying', 'displays', 'disposed', 'disposition', 'dispositions', 'dispute', 'disquiet', 'disquieted', 'disquisition', 'disquisitions', 'disregard', 'dissect', 'dissecting', 'dissipate', 'dissipated', 'dissipates', 'dissoluble', 'dissuade', 'distance', 'distant', 'distaste', 'distemper', 'distinct', 'distinction', 'distinctly', 'distinguish', 'distinguished', 'distinguishing', 'distorted', 'distraction', 'distress', 'distressing', 'distributed', 'distributing', 'district', 'distrust', 'distrusted', 'disturb', 'disturbed', 'disturbs', 'disunion', 'diversity', 'divert', 'diverted', 'divine', 'divinely', 'divinest', 'division', 'divulged', 'dizzy', 'do', 'docile', 'does', 'dog', 'dogmatism', 'dogs', 'doing', 'dome', 'domes', 'domestic', 'dominion', 'dominions', 'done', 'doomed', 'door', 'doors', 'dormant', 'doted', 'doth', 'doting', 'double', 'doubly', 'doubt', 'doubted', 'doubtful', 'doubtless', 'doubts', 'down', 'downcast', 'downstairs', 'dozen', 'dozing', 'drag', 'dragged', 'dragging', 'drance', 'draught', 'draw', 'drawer', 'drawing', 'drawn', 'dread', 'dreaded', 'dreadful', 'dreadfully', 'dreading', 'dream', 'dreaming', 'dreams', 'dreamt', 'dreary', 'drenched', 'dress', 'dressed', 'drew', 'dried', 'drifted', 'drifting', 'drink', 'drive', 'driven', 'drivest', 'drop', 'dropped', 'dropping', 'drops', 'dross', 'drove', 'drowned', 'drug', 'drunk', 'drunken', 'dry', 'du', 'due', 'dull', 'dun', 'dungeon', 'dungeons', 'duration', 'during', 'dusk', 'dusky', 'dust', 'dutch', 'duties', 'duty', 'duvillard', 'dwell', 'dwelling', 'dwelt', 'dying', 'each', 'eager', 'eagerly', 'eagerness', 'eagle', 'ear', 'earlier', 'earliest', 'early', 'earn', 'earnest', 'earnestly', 'earnestness', 'ears', 'earth', 'earthquake', 'ease', 'easier', 'easily', 'east', 'eastern', 'eat', 'eaten', 'ebook', 'eccentricities', 'echoed', 'ecstasy', 'ecstatic', 'edge', 'edges', 'edinburgh', 'educate', 'educated', 'education', 'efface', 'effect', 'effected', 'effects', 'effectual', 'effort', 'effusions', 'eight', 'eighteenth', 'either', 'elapsed', 'elasticity', 'elder', 'eldest', 'electricity', 'element', 'elemental', 'elementary', 'elements', 'elevate', 'elevated', 'elevates', 'elevating', 'elevation', 'eleven', 'elixir', 'elizabeth', 'elizabeth’s', 'eloquence', 'eloquent', 'else', 'elude', 'eluded', 'emaciated', 'embark', 'embarkation', 'embarked', 'embarks', 'embers', 'embittered', 'emblem', 'embosomed', 'embrace', 'embraced', 'emergencies', 'emergency', 'emigration', 'eminently', 'emotion', 'emotions', 'empire', 'empires', 'employ', 'employed', 'employment', 'employments', 'empty', 'emulate', 'emulation', 'enable', 'enabled', 'enchanted', 'enchanting', 'enchantment', 'encomiums', 'encompassed', 'encounter', 'encountered', 'encountering', 'encourage', 'encouraged', 'encouraging', 'end', 'endangered', 'endeared', 'endeavour', 'endeavoured', 'endeavouring', 'endeavours', 'ended', 'ending', 'endless', 'endow', 'endowed', 'endowments', 'endued', 'endurance', 'endure', 'endured', 'enduring', 'enemies', 'enemy', 'energetically', 'energies', 'energy', 'enfranchised', 'engage', 'engaged', 'engagement', 'engages', 'engaging', 'england', 'english', 'englishman', 'englishmen', 'engrossed', 'enhanced', 'enigmatic', 'enjoined', 'enjoy', 'enjoyed', 'enjoying', 'enjoyment', 'enjoyments', 'enjoys', 'enkindled', 'enlightened', 'ennui', 'enormity', 'enough', 'enounced', 'enquired', 'enraged', 'enraptured', 'enslave', 'enslaved', 'ensued', 'ensuing', 'ensure', 'enter', 'entered', 'entering', 'enterprise', 'enters', 'entertain', 'entertained', 'enthusiasm', 'enthusiastic', 'enticed', 'enticement', 'enticements', 'enticing', 'entire', 'entirely', 'entitled', 'entrance', 'entranced', 'entrancingly', 'entreat', 'entreated', 'entreaties', 'entreating', 'entrench', 'enunciation', 'envelop', 'enveloped', 'environs', 'envy', 'ephemeral', 'epithets', 'epoch', 'equal', 'equalled', 'equally', 'equals', 'equitable', 'era', 'eradicated', 'eradicating', 'erect', 'ernest', 'erroneous', 'erroneously', 'errors', 'escape', 'escaped', 'escapes', 'especial', 'especially', 'esq', 'established', 'esteem', 'esteemed', 'eternal', 'eternally', 'eternity', 'eulogy', 'europe', 'european', 'evaded', 'eve', 'even', 'evening', 'event', 'eventful', 'events', 'eventual', 'ever', 'everlasting', 'every', 'everybody', 'everyday', 'everyone', 'everything', 'everywhere', 'evian', 'evidence', 'evidently', 'evil', 'evils', 'evinced', 'exactly', 'exalted', 'examination', 'examine', 'examined', 'examining', 'example', 'exasperate', 'exasperated', 'exceed', 'exceeded', 'exceedingly', 'excellence', 'excellent', 'except', 'exception', 'excess', 'excessive', 'excessively', 'exchange', 'exchanged', 'excite', 'excited', 'excitements', 'excites', 'exciting', 'exclaim', 'exclaimed', 'exclamation', 'exclamations', 'excluded', 'excommunication', 'exculpated', 'excursion', 'excuse', 'execrate', 'execrated', 'execration', 'execute', 'executed', 'executing', 'execution', 'exemplified', 'exempt', 'exercise', 'exercised', 'exert', 'exerted', 'exerting', 'exertion', 'exertions', 'exhausted', 'exhaustion', 'exhibit', 'exhibited', 'exhilarated', 'exhortations', 'exile', 'exist', 'existed', 'existence', 'existing', 'exists', 'exordium', 'exotic', 'expanded', 'expanding', 'expanse', 'expect', 'expectation', 'expectations', 'expected', 'expedite', 'expedition', 'expeditions', 'experience', 'experienced', 'experiment', 'experimentalist', 'experiments', 'expiration', 'expire', 'explain', 'explained', 'explaining', 'explanation', 'explanations', 'exploded', 'exploit', 'explore', 'exposed', 'exposing', 'expostulate', 'express', 'expressed', 'expression', 'expressions', 'expressive', 'exquisite', 'exquisitely', 'extended', 'extensive', 'extent', 'extents', 'external', 'extinct', 'extinction', 'extinguish', 'extinguished', 'extort', 'extract', 'extracting', 'extraordinary', 'extreme', 'extremely', 'extremes', 'extremest', 'extremities', 'extremity', 'extricate', 'exult', 'exultation', 'exulting', 'eye', 'eyeballs', 'eyed', 'eyelashes', 'eyes', 'face', 'faces', 'facile', 'facilitated', 'facility', 'fact', 'facts', 'faculties', 'faculty', 'fade', 'faded', 'fail', 'failed', 'failing', 'failure', 'faint', 'fainted', 'fainter', 'fainting', 'faintness', 'fair', 'fairer', 'fairest', 'fairly', 'fairy', 'faith', 'faithful', 'falkland', 'fall', 'fallen', 'falling', 'false', 'falsehood', 'falsely', 'faltering', 'fame', 'famed', 'familiar', 'familiarised', 'familiarity', 'familiarly', 'families', 'family', 'famine', 'fan', 'fancied', 'fancies', 'fanciful', 'fancy', 'fancying', 'fangs', 'fanned', 'far', 'fare', 'farewell', 'farm', 'farmer', 'farmhouse', 'farther', 'fashion', 'fashioned', 'fast', 'fastidious', 'fatal', 'fatality', 'fatally', 'fate', 'fated', 'father', 'father’s', 'fatigue', 'fatigued', 'fatigues', 'fatiguing', 'faultiness', 'faults', 'faulty', 'favour', 'favourable', 'favourite', 'favourites', 'fear', 'feared', 'fearful', 'fearfully', 'fearing', 'fearless', 'fears', 'feature', 'features', 'february', 'fee', 'feeble', 'feebly', 'feel', 'feeling', 'feelings', 'feels', 'feet', 'feint', 'felix', 'fell', 'fellow', 'fellows', 'fellowship', 'felt', 'female', 'females', 'feminine', 'fertile', 'fervent', 'fervently', 'fervour', 'festering', 'festival', 'fetter', 'fettered', 'fever', 'feverish', 'few', 'fibre', 'fibres', 'fidelity', 'field', 'fields', 'fiend', 'fiendish', 'fiend’s', 'fierce', 'fierceness', 'fifteen', 'fifth', 'fifty', 'fight', 'figure', 'figures', 'filial', 'fill', 'filled', 'fills', 'film', 'filthy', 'final', 'finally', 'find', 'finding', 'finds', 'fine', 'finest', 'finger', 'fingers', 'finish', 'finished', 'fire', 'fired', 'firesides', 'firing', 'firm', 'firmest', 'firmly', 'firmness', 'first', 'fish', 'fishermen', 'fishers', 'fishing', 'fit', 'fitness', 'fits', 'fitted', 'fitter', 'fitting', 'five', 'fix', 'fixed', 'fixing', 'flagrant', 'flame', 'flames', 'flannel', 'flash', 'flashed', 'flashes', 'flat', 'fled', 'flesh', 'flew', 'flight', 'flit', 'flitted', 'float', 'floated', 'floating', 'flood', 'floor', 'florins', 'floundering', 'flourished', 'flourishing', 'flow', 'flowed', 'flower', 'flowers', 'flowery', 'flowing', 'flows', 'fluctuate', 'fluctuating', 'flung', 'flushed', 'fly', 'flying', 'foe', 'foes', 'fog', 'foldings', 'folds', 'foliage', 'folks', 'follow', 'followed', 'followers', 'following', 'follows', 'folly', 'fond', 'fondly', 'fondness', 'food', 'fool', 'foolish', 'foot', 'footed', 'footsteps', 'for', 'forbear', 'forbid', 'forbidden', 'force', 'forced', 'forces', 'forcible', 'forcibly', 'forcing', 'forebodings', 'forehead', 'foreign', 'foresaw', 'forest', 'forests', 'foretaste', 'forget', 'forgetfulness', 'forgetting', 'forgive', 'forgo', 'forgot', 'forgotten', 'forked', 'form', 'formation', 'formed', 'former', 'formerly', 'formidable', 'forms', 'forsaken', 'forsakes', 'fort', 'forth', 'fortifications', 'fortify', 'fortitude', 'fortnight', 'fortunate', 'fortunately', 'fortune', 'fortunes', 'forward', 'foster', 'fosterage', 'fought', 'found', 'foundations', 'founded', 'founders', 'fountain', 'four', 'fourteen', 'fragment', 'frail', 'frame', 'framed', 'france', 'frank', 'frankenstein', 'frankness', 'frantic', 'fraud', 'fraught', 'free', 'freed', 'freedom', 'freely', 'freezing', 'frementi', 'french', 'frenchwoman', 'frenzy', 'frequent', 'frequently', 'fresh', 'fretting', 'friend', 'friendless', 'friends', 'friendship', 'frightened', 'frightful', 'fringed', 'frogs', 'from', 'frontiers', 'frost', 'frosts', 'frosty', 'frowning', 'frowns', 'frozen', 'fruitless', 'fruitlessly', 'fuel', 'fugitives', 'fulfil', 'fulfilled', 'fulfilling', 'fulfilment', 'full', 'fully', 'functions', 'fund', 'funeral', 'furies', 'furious', 'furiously', 'furnished', 'furniture', 'furs', 'further', 'furtherance', 'fury', 'futile', 'futility', 'future', 'futurity', 'gaiety', 'gain', 'gained', 'gait', 'gale', 'gales', 'gall', 'gallant', 'gallery', 'galvanism', 'game', 'gaolers', 'garb', 'garden', 'gardener', 'gardens', 'gasped', 'gates', 'gather', 'gathered', 'gaunt', 'gave', 'gay', 'gaze', 'gazed', 'gazes', 'gazing', 'general', 'generally', 'generation', 'generations', 'generosity', 'generous', 'geneva', 'genevan', 'genevese', 'genial', 'genius', 'gentle', 'gentleman', 'gentleness', 'gently', 'geography', 'german', 'germans', 'germany', 'gesticulations', 'gesture', 'gestures', 'get', 'getting', 'ghastly', 'ghosts', 'giant', 'gibe', 'gift', 'gigantic', 'gilded', 'girl', 'give', 'given', 'giver', 'gives', 'giving', 'glacier', 'glaciers', 'glad', 'gladly', 'gladness', 'glance', 'glared', 'glaring', 'glens', 'glide', 'glided', 'glimmer', 'glimmering', 'glimmers', 'glimpse', 'glittering', 'globe', 'gloom', 'gloomily', 'gloomy', 'gloried', 'glorious', 'glory', 'glow', 'glowed', 'glowing', 'glut', 'glutted', 'gnashed', 'gnashes', 'gnashing', 'go', 'god', 'godlike', 'gods', 'godwin', 'god’s', 'going', 'gold', 'golden', 'gone', 'good', 'goodness', 'goring', 'gospel', 'gossip', 'governed', 'governing', 'government', 'governments', 'grace', 'graceful', 'grades', 'gradually', 'grand', 'grandeur', 'grant', 'grapple', 'grappling', 'grasp', 'grasped', 'grasping', 'grass', 'grate', 'grated', 'grateful', 'gratification', 'gratified', 'gratify', 'gratifying', 'gratitude', 'grave', 'graves', 'gravesend', 'gre', 'great', 'greater', 'greatest', 'greatly', 'greatness', 'grecians', 'greece', 'greedily', 'greek', 'greeks', 'green', 'greenland', 'greenwich', 'greeting', 'grew', 'grey', 'grief', 'griefs', 'grieve', 'grieved', 'grievously', 'grin', 'groan', 'groaned', 'groans', 'ground', 'groundwork', 'group', 'grovel', 'grow', 'grown', 'growth', 'grudge', 'gruff', 'guarded', 'guardian', 'guardians', 'guards', 'guess', 'guessed', 'guessing', 'guest', 'guidance', 'guide', 'guided', 'guiding', 'guile', 'guilt', 'guiltless', 'guiltlessness', 'guilty', 'guise', 'guitar', 'gun', 'gurgling', 'gush', 'gushed', 'gutenberg', 'habit', 'habitable', 'habitation', 'habitations', 'habits', 'had', 'hadst', 'haggard', 'hail', 'hailed', 'hair', 'hairs', 'half', 'halfway', 'hall', 'halo', 'hamlet', 'hampden', 'hand', 'handed', 'handkerchief', 'handle', 'hands', 'handsome', 'handwriting', 'hanging', 'hangman', 'hangs', 'hapless', 'happen', 'happened', 'happening', 'happier', 'happily', 'happiness', 'happy', 'harbour', 'hard', 'harden', 'hardened', 'harder', 'hardly', 'hardship', 'hardships', 'hardy', 'hare', 'harem', 'harm', 'harmless', 'harmony', 'harnessed', 'harrowing', 'harsh', 'harvest', 'has', 'hast', 'haste', 'hasten', 'hastened', 'hastily', 'hasty', 'hate', 'hated', 'hateful', 'hatred', 'haughty', 'haunt', 'haunted', 'have', 'having', 'havoc', 'havre', 'hay', 'hazard', 'he', 'head', 'heal', 'healed', 'health', 'hear', 'heard', 'hearer', 'hearers', 'hearing', 'heart', 'hearted', 'heartfelt', 'heartily', 'heartless', 'hearts', 'heat', 'heath', 'heaths', 'heatless', 'heaven', 'heavenly', 'heavens', 'heavier', 'heavily', 'heaving', 'heavy', 'hedges', 'heed', 'heeded', 'height', 'held', 'hell', 'hellish', 'help', 'helped', 'helpless', 'helplessness', 'hemisphere', 'hence', 'henceforth', 'henry', 'her', 'herb', 'herbage', 'herd', 'herds', 'here', 'hereafter', 'hero', 'heroes', 'heroic', 'heroical', 'heroism', 'hers', 'herself', 'hesitate', 'hesitated', 'hid', 'hidden', 'hide', 'hideous', 'hideously', 'hideousness', 'hides', 'hiding', 'high', 'higher', 'highest', 'highlands', 'highly', 'hilarity', 'hill', 'hills', 'him', 'himself', 'hindrance', 'hinges', 'hire', 'hired', 'his', 'historical', 'histories', 'history', 'hitherto', 'hoarse', 'hoarser', 'hold', 'holding', 'holds', 'holiday', 'holland', 'holy', 'home', 'homeless', 'homer', 'homeward', 'honest', 'honour', 'honourable', 'honoured', 'hope', 'hoped', 'hopeless', 'hopes', 'hoping', 'horizon', 'horrible', 'horrid', 'horror', 'horrors', 'horseback', 'horses', 'hospitality', 'host', 'hot', 'hour', 'hours', 'hour’s', 'house', 'household', 'houses', 'hovel', 'hovels', 'hover', 'hovered', 'hovers', 'how', 'however', 'howl', 'howlings', 'hue', 'huge', 'human', 'humane', 'humanity', 'humankind', 'humid', 'humour', 'hundred', 'hundredfold', 'hundredth', 'hung', 'hunger', 'hungry', 'hunt', 'hunted', 'hurricane', 'hurried', 'hurries', 'hurry', 'hurt', 'husband', 'hushed', 'hut', 'huts', 'hypocritical', 'hysterics', 'i', 'ice', 'ices', 'icy', 'idea', 'ideal', 'ideas', 'identify', 'idle', 'idleness', 'idler', 'idol', 'if', 'ignoble', 'ignominious', 'ignominy', 'ignorance', 'ignorant', 'ignorantly', 'ill', 'illiterate', 'illness', 'illuminate', 'illuminated', 'illuminating', 'illustrate', 'illustrated', 'illustrious', 'image', 'imaged', 'images', 'imaginary', 'imagination', 'imaginations', 'imaginative', 'imagine', 'imagined', 'imbibed', 'imbued', 'imitate', 'imitation', 'immaculate', 'immeasurable', 'immeasurably', 'immediate', 'immediately', 'immense', 'immensity', 'immersed', 'imminent', 'immoderate', 'immortal', 'immortality', 'immured', 'immutable', 'imparted', 'imparting', 'impassable', 'impassive', 'impatience', 'impatient', 'impatiently', 'impediment', 'impediments', 'impelled', 'impend', 'impending', 'impenetrable', 'imperatively', 'imperceptible', 'imperfect', 'imperial', 'imperious', 'impertinent', 'impervious', 'impetuous', 'implements', 'implores', 'imply', 'importance', 'important', 'imposed', 'imposing', 'impossibilities', 'impossibility', 'impossible', 'impotence', 'impotent', 'impracticability', 'impracticable', 'imprecate', 'imprecations', 'impress', 'impressed', 'impression', 'impressions', 'impressive', 'imprinted', 'imprisonment', 'improbable', 'improved', 'improvement', 'improvements', 'imprudence', 'imprudently', 'impulse', 'impulses', 'in', 'inaccessible', 'inaction', 'inadequate', 'inanimate', 'inapplicable', 'inarticulate', 'inasmuch', 'incalculable', 'incantations', 'incapable', 'incessantly', 'incident', 'incidents', 'incipient', 'incitement', 'inciting', 'inclemency', 'inclination', 'inclinations', 'incline', 'inclined', 'include', 'included', 'includes', 'including', 'incoherent', 'incommoded', 'incomplete', 'inconceivable', 'inconsiderate', 'inconstant', 'inconvenience', 'inconveniences', 'increase', 'increased', 'increases', 'increasing', 'incredible', 'incredulity', 'incredulous', 'incurable', 'indebted', 'indecent', 'indecision', 'indeed', 'indefatigable', 'indelible', 'indelibly', 'independence', 'india', 'indian', 'indicated', 'indicating', 'indications', 'indifference', 'indifferent', 'indignant', 'indignation', 'indiscriminately', 'indispensable', 'indistinct', 'indolence', 'induce', 'induced', 'indulge', 'indulged', 'indulgence', 'indulging', 'industrious', 'ineffectual', 'inequalities', 'inestimable', 'inevitable', 'inexhaustible', 'inexorable', 'inexperience', 'inexperienced', 'inexpressible', 'inextinguishable', 'infallible', 'infallibly', 'infamy', 'infancy', 'infant', 'infantile', 'infantine', 'infatuation', 'inferior', 'inferiors', 'infidels', 'infinite', 'infinitely', 'infinity', 'infirmities', 'inflamed', 'inflict', 'inflicted', 'infliction', 'influence', 'influenced', 'inform', 'information', 'informed', 'infuse', 'infused', 'infusing', 'ingenuity', 'inglorious', 'ingolstadt', 'ingratitude', 'inhabit', 'inhabitant', 'inhabitants', 'inhabited', 'inhabits', 'inheritance', 'inherited', 'inhospitably', 'inhuman', 'injunction', 'injure', 'injured', 'injurer', 'injuries', 'injury', 'injustice', 'inmate', 'inmates', 'inmost', 'inn', 'inner', 'innocence', 'innocent', 'innumerable', 'inquietude', 'inquired', 'inquirer', 'inquirers', 'inquiries', 'inquiring', 'inquisitive', 'inquisitiveness', 'inroads', 'insanity', 'insatiable', 'insatiate', 'inscription', 'inscriptions', 'insect', 'insensible', 'inside', 'insight', 'insisted', 'insolent', 'inspecting', 'inspire', 'inspired', 'inspiring', 'inspirited', 'inspiriting', 'instance', 'instances', 'instant', 'instantly', 'instants', 'instead', 'instigate', 'instigated', 'instinct', 'instinctively', 'institutions', 'instructed', 'instructing', 'instruction', 'instructions', 'instructor', 'instructors', 'instrument', 'instruments', 'insufficient', 'insulted', 'insultingly', 'insuperable', 'insupportable', 'insurance', 'insurmountable', 'insurrection', 'integrity', 'intellect', 'intellectual', 'intelligence', 'intend', 'intended', 'intense', 'intensity', 'intention', 'intentions', 'intently', 'intercept', 'intercepted', 'interchange', 'interchanging', 'intercourse', 'interest', 'interested', 'interesting', 'interests', 'interfere', 'interfered', 'interference', 'interment', 'intermixed', 'internal', 'interpret', 'interpretation', 'interpreted', 'interpreter', 'interrupt', 'interrupted', 'interruption', 'intersected', 'interspersed', 'intertwined', 'interval', 'intervals', 'intervened', 'intervening', 'interview', 'intimacy', 'intimate', 'intimated', 'intimidated', 'into', 'intolerable', 'intonations', 'intoxicating', 'intricacies', 'introduce', 'introduced', 'introducing', 'introduction', 'intrude', 'intrusion', 'intuitive', 'inuring', 'invade', 'invader', 'invective', 'invented', 'investigating', 'invigorated', 'invincible', 'invisible', 'invitation', 'invoked', 'involuntarily', 'invulnerable', 'ireland', 'irish', 'irksome', 'iron', 'irradiated', 'irradiation', 'irregular', 'irremediable', 'irreparable', 'irreproachable', 'irresistible', 'irresolute', 'irresolution', 'irretrievable', 'irretrievably', 'irrevocably', 'irritability', 'is', 'isaac', 'isis', 'island', 'islands', 'isle', 'issue', 'issued', 'issuing', 'it', 'italian', 'italians', 'italy', 'its', 'itself', 'jacket', 'jaws', 'jeer', 'jewel', 'jewels', 'john', 'join', 'joined', 'joint', 'joints', 'journal', 'journey', 'journeying', 'joy', 'joyful', 'joyous', 'joys', 'judge', 'judged', 'judgement', 'judges', 'judgment', 'july', 'jumped', 'june', 'junior', 'jura', 'juras', 'jury', 'just', 'justice', 'justified', 'justify', 'justine', 'justine’s', 'jutting', 'keel', 'keen', 'keep', 'keeping', 'kennel', 'kept', 'keys', 'kicked', 'kid', 'kill', 'killed', 'kind', 'kinder', 'kindest', 'kindle', 'kindled', 'kindliness', 'kindling', 'kindly', 'kindness', 'kinds', 'king', 'kingdoms', 'kings', 'kinsman', 'kirwin', 'kirwin’s', 'kiss', 'kissed', 'kitchen', 'kneel', 'kneeling', 'knees', 'knell', 'knelt', 'knew', 'knightly', 'knocked', 'know', 'knowing', 'knowledge', 'known', 'knows', 'krempe', 'la', 'laboratory', 'laborious', 'labour', 'labourers', 'labours', 'lacey', 'ladies', 'lady', 'laid', 'lake', 'lakes', 'lamb', 'lament', 'lamentations', 'lamented', 'lamp', 'land', 'landed', 'landing', 'lands', 'landscape', 'language', 'languages', 'languid', 'languishing', 'languor', 'lantern', 'lap', 'lapse', 'large', 'lashes', 'lassitude', 'last', 'lasted', 'lastly', 'late', 'lately', 'later', 'latitude', 'latter', 'latterly', 'laudanum', 'laugh', 'laughed', 'laughing', 'laughter', 'lausanne', 'lavenza', 'law', 'lawgivers', 'lawless', 'laws', 'lay', 'laying', 'le', 'lead', 'leader', 'leaf', 'league', 'leagues', 'leak', 'lean', 'leaning', 'leaped', 'learn', 'learned', 'learning', 'learnt', 'least', 'leathern', 'leave', 'leaved', 'leaves', 'leaving', 'lecture', 'lectures', 'lecturing', 'led', 'left', 'leghorn', 'legible', 'leisure', 'lend', 'length', 'less', 'lessened', 'lessening', 'lesson', 'lessons', 'lest', 'let', 'letter', 'letters', 'letting', 'level', 'liable', 'liberal', 'liberally', 'liberated', 'liberty', 'library', 'lichen', 'licked', 'lids', 'lie', 'lies', 'lieutenant', 'life', 'lifeless', 'lifelessness', 'lifted', 'ligaments', 'light', 'lighted', 'lightened', 'lighter', 'lighthearted', 'lightning', 'lightnings', 'lights', 'like', 'likely', 'limb', 'limbs', 'limit', 'line', 'lineaments', 'linen', 'lines', 'lingered', 'lingering', 'link', 'linked', 'lion', 'lips', 'lissier', 'list', 'listen', 'listened', 'listener', 'listener’s', 'listening', 'listless', 'listlessly', 'literally', 'literary', 'literature', 'little', 'littleness', 'live', 'lived', 'lively', 'lives', 'livid', 'living', 'load', 'loaded', 'loaf', 'loathed', 'loathing', 'loathsome', 'localities', 'lock', 'locking', 'locks', 'lofty', 'loitered', 'london', 'lonely', 'long', 'longed', 'longer', 'longing', 'look', 'looked', 'looking', 'looks', 'loose', 'lord', 'lords', 'lose', 'loss', 'lost', 'lot', 'loud', 'loudly', 'loudness', 'louis', 'louisa', 'love', 'loved', 'lovedst', 'loveliness', 'lovely', 'lover', 'lovers', 'low', 'lower', 'lowest', 'lucerne', 'lukewarm', 'lullaby', 'lulled', 'lulling', 'lurked', 'lustrous', 'luxuriances', 'luxuriant', 'luxuries', 'luxurious', 'luxury', 'lycurgus', 'lying', 'lyons', 'm', 'machinations', 'machines', 'mad', 'madame', 'maddening', 'made', 'madly', 'madman', 'madness', 'magic', 'magistrate', 'magnet', 'magnificence', 'magnificent', 'magnitude', 'magnus', 'mainland', 'maintained', 'maintenance', 'mainz', 'majestic', 'majesty', 'make', 'maker', 'makes', 'making', 'maladie', 'malice', 'malicious', 'malignant', 'malignity', 'man', 'manacled', 'mandate', 'mangled', 'manifested', 'manifold', 'mankind', 'manly', 'manner', 'manners', 'mannheim', 'manoir', 'manon', 'mansfield', 'mantel', 'manuscript', 'many', 'man’s', 'map', 'march', 'margaret', 'mariner', 'mark', 'marked', 'market', 'marking', 'marks', 'marriage', 'married', 'marrying', 'martyrs', 'marvellous', 'mary', 'masquerades', 'mass', 'massacred', 'massacring', 'masses', 'master', 'masters', 'match', 'mate', 'material', 'materially', 'materials', 'maternal', 'mates', 'mathematics', 'matlock', 'matter', 'matters', 'maw', 'may', 'maybe', 'me', 'meadows', 'meal', 'mean', 'meandering', 'meanest', 'meaning', 'meanly', 'means', 'meant', 'meantime', 'meanwhile', 'measure', 'measured', 'measures', 'mechanical', 'mechanics', 'mechanism', 'mediation', 'medical', 'medicine', 'medicines', 'meditate', 'mediterranean', 'medium', 'meed', 'meet', 'meeting', 'melancholy', 'melbourne', 'melt', 'memorable', 'memory', 'men', 'menaced', 'menaces', 'mental', 'mention', 'mentioned', 'mentioning', 'mercenary', 'merchant', 'merchantman', 'merchants', 'merchant’s', 'merciless', 'mercy', 'mere', 'merely', 'merit', 'merits', 'met', 'metals', 'metaphysical', 'method', 'methods', 'mexico', 'microscope', 'middle', 'midnight', 'midst', 'mien', 'might', 'mightier', 'mighty', 'milan', 'milanese', 'mild', 'mildly', 'mildness', 'mile', 'miles', 'military', 'milk', 'mimic', 'mind', 'minded', 'minds', 'mine', 'mines', 'mingled', 'mingling', 'miniature', 'minister', 'ministered', 'ministers', 'minute', 'minutely', 'minuteness', 'minutes', 'minutest', 'minutiae', 'miracle', 'miracles', 'miraculous', 'mirror', 'mirrored', 'mischances', 'mischief', 'misdeed', 'miserable', 'miserably', 'miseries', 'misery', 'misfortune', 'misfortunes', 'misled', 'miss', 'missed', 'missile', 'mist', 'mistake', 'mistaken', 'mistress', 'mists', 'misty', 'mix', 'mixture', 'mock', 'mockery', 'mode', 'model', 'moderate', 'moderation', 'modern', 'modest', 'modesty', 'modified', 'modulated', 'mole', 'moment', 'momentarily', 'momentary', 'moments', 'mon', 'monarchies', 'monday', 'money', 'monium', 'monotonous', 'mons', 'monster', 'monsters', 'monstrous', 'mont', 'montal', 'montanvert', 'month', 'months', 'months’', 'monument', 'monuments', 'mon’s', 'mood', 'moon', 'moonlight', 'moonshine', 'moral', 'moralizing', 'more', 'moritz', 'morning', 'morning’s', 'morrow', 'mortal', 'mortals', 'mortification', 'most', 'mother', 'mother’s', 'motion', 'motioned', 'motionless', 'motions', 'motive', 'motives', 'mould', 'moulded', 'moulding', 'mountain', 'mountaineers', 'mountainous', 'mountains', 'mountain’s', 'mounted', 'mourn', 'mourner', 'mournful', 'mournfully', 'mourning', 'move', 'moved', 'moving', 'mr', 'mrs', 'much', 'muhammad', 'muhammadan', 'mule', 'multifarious', 'multiplicity', 'multiplied', 'multitude', 'mummy', 'murder', 'murdered', 'murderer', 'murderer’s', 'murderess', 'murdering', 'murderous', 'murder’s', 'murmur', 'murmured', 'murmuring', 'muscle', 'muscles', 'music', 'musical', 'must', 'musty', 'mutability', 'mutable', 'mute', 'mutilated', 'mutiny', 'muttered', 'mutual', 'my', 'myriads', 'myself', 'mysteries', 'mysterious', 'mystery', 'n', 'name', 'named', 'nameless', 'names', 'naples', 'narrated', 'narration', 'narrations', 'narrative', 'narrow', 'narrowed', 'narrower', 'nation', 'national', 'nations', 'native', 'natural', 'nature', 'natures', 'naval', 'navigators', 'nay', 'ne', 'near', 'nearer', 'nearly', 'neat', 'neater', 'necessarily', 'necessary', 'necessity', 'neck', 'need', 'needed', 'needle', 'neglect', 'neglected', 'negligently', 'negotiation', 'neighbourhood', 'neighbouring', 'neighbours', 'neither', 'nerves', 'nervous', 'nets', 'never', 'nevertheless', 'new', 'news', 'newton', 'next', 'ne’er', 'nicer', 'niche', 'niece', 'night', 'nightingale', 'nightly', 'nightmare', 'nights', 'night’s', 'nine', 'no', 'noble', 'nobleman', 'noblest', 'nocturnal', 'noise', 'noisome', 'noisy', 'none', 'nonsense', 'nook', 'noon', 'nor', 'north', 'northeast', 'northerly', 'northern', 'northward', 'northwards', 'not', 'noted', 'notes', 'nothing', 'notice', 'notwithstanding', 'nought', 'nourished', 'nourishment', 'novelties', 'novelty', 'november', 'now', 'nugent', 'numa', 'number', 'numerous', 'nuptial', 'nurse', 'nursed', 'nuts', 'o', 'oak', 'oaks', 'oar', 'oars', 'oaten', 'oath', 'oatmeal', 'obdurate', 'obedience', 'obedient', 'obey', 'obeying', 'object', 'objects', 'oblige', 'obliged', 'obliterate', 'obliterated', 'oblivion', 'obnoxious', 'obscure', 'obscured', 'obscurely', 'observations', 'observe', 'observed', 'observer', 'observing', 'obstacle', 'obstacles', 'obstinate', 'obstructed', 'obtain', 'obtained', 'obtaining', 'obvious', 'occasion', 'occasioned', 'occasions', 'occupation', 'occupations', 'occupied', 'occupy', 'occur', 'occurred', 'occurrence', 'occurrences', 'ocean', 'october', 'odious', 'of', 'off', 'offals', 'offer', 'offered', 'offering', 'offers', 'office', 'officer', 'offices', 'officially', 'offspring', 'often', 'oftener', 'ognor', 'ogre', 'oh', 'old', 'older', 'omen', 'ominous', 'omit', 'omitted', 'omnipotence', 'omnipotent', 'on', 'once', 'one', 'ones', 'only', 'onwards', 'opaque', 'open', 'opened', 'opening', 'openly', 'operate', 'operation', 'operations', 'opinion', 'opinions', 'opportunity', 'opposed', 'opposing', 'opposite', 'opposition', 'oppressed', 'oppresses', 'oppression', 'oppressive', 'opprobrium', 'or', 'orb', 'orbs', 'order', 'ordered', 'orders', 'ordinary', 'organization', 'organs', 'oriental', 'orientalists', 'origin', 'original', 'orkney', 'orkneys', 'orphan', 'other', 'others', 'otherwise', 'other’s', 'ought', 'our', 'ours', 'ourselves', 'out', 'outcast', 'outhouse', 'outlines', 'outraged', 'outrages', 'outside', 'outstript', 'outward', 'over', 'overcame', 'overcast', 'overcome', 'overflowed', 'overflowing', 'overhanging', 'overhangs', 'overhung', 'overjoyed', 'overlook', 'overlooked', 'overlooking', 'overlooks', 'overpowered', 'overpowering', 'overshadowed', 'overspread', 'overtake', 'overtaxed', 'overthrow', 'overweigh', 'overwhelm', 'overwhelmed', 'overwhelming', 'owe', 'owed', 'owes', 'owest', 'owing', 'own', 'owner', 'owning', 'oxford', 'o’clock', 'p', 'pace', 'pacific', 'pacing', 'pack', 'packed', 'packet', 'paddling', 'page', 'paid', 'pail', 'pain', 'pained', 'painful', 'painfully', 'pains', 'painstaking', 'painted', 'painters', 'palace', 'palaces', 'pale', 'pallid', 'palpable', 'palpitate', 'palpitated', 'palpitation', 'pand', 'panegyric', 'panes', 'pang', 'pangs', 'panic', 'papa', 'paper', 'papers', 'paracelsus', 'paradise', 'paradisiacal', 'paramount', 'parched', 'pardon', 'pardoning', 'parent', 'parents', 'parents’', 'paris', 'parliament', 'paroxysm', 'paroxysms', 'part', 'parted', 'partiality', 'partially', 'participate', 'participated', 'particularly', 'particulars', 'parties', 'partly', 'parts', 'party', 'pass', 'passage', 'passages', 'passed', 'passes', 'passing', 'passion', 'passionate', 'passionately', 'passions', 'passive', 'passports', 'past', 'pasture', 'patches', 'paternal', 'path', 'pathetic', 'pathless', 'paths', 'pathways', 'patience', 'patient', 'patiently', 'patriarchal', 'patriot', 'pattered', 'paul’s', 'pause', 'paused', 'pauses', 'pausing', 'pay', 'paying', 'pays', 'peace', 'peaceable', 'peaceably', 'peaceful', 'peak', 'peaked', 'peaks', 'pearly', 'peasant', 'peasants', 'peasant’s', 'pebble', 'peculiar', 'peculiarly', 'pedantry', 'pedestrian', 'peeped', 'peeping', 'pen', 'penalty', 'penetrate', 'penetrated', 'penetration', 'penniless', 'pensive', 'pentland', 'penury', 'people', 'peopled', 'perambulations', 'perceive', 'perceived', 'perceiving', 'perceptible', 'perceptibly', 'perceptions', 'perdition', 'perfect', 'perfection', 'perfectionate', 'perfectly', 'perform', 'performed', 'performs', 'perhaps', 'peril', 'perilous', 'period', 'periodically', 'periods', 'perish', 'perished', 'permission', 'permit', 'permits', 'permitted', 'perpendicular', 'perpendicularity', 'perpendicularly', 'perpetrate', 'perpetrated', 'perpetual', 'perpetually', 'perplexed', 'persecuted', 'persecutor', 'perseverance', 'persevere', 'persevering', 'persian', 'persisted', 'person', 'personal', 'personally', 'persons', 'persuade', 'persuaded', 'persuades', 'persuading', 'persuasion', 'persuasions', 'persuasive', 'perth', 'pertinacity', 'perturbed', 'peru', 'perused', 'pervaded', 'perversity', 'pest', 'petersburgh', 'petticoat', 'petty', 'phenomena', 'philosopher', 'philosophers', 'philosopher’s', 'philosophical', 'philosophy', 'phrase', 'phraseology', 'physical', 'physician', 'physiognomy', 'physiology', 'picked', 'picking', 'picture', 'pictured', 'pictures', 'picturesque', 'piece', 'pieces', 'pierce', 'pierced', 'piercing', 'pig', 'pile', 'pilgrimage', 'pillow', 'pine', 'pines', 'pink', 'pinnacle', 'piny', 'pioneer', 'pistol', 'pistols', 'pitchy', 'pitiable', 'pitied', 'pities', 'pitiless', 'pittance', 'pity', 'place', 'placed', 'places', 'placid', 'placing', 'plain', 'plainly', 'plainpalais', 'plains', 'plaited', 'plan', 'plank', 'planks', 'plans', 'plants', 'play', 'played', 'playfellow', 'playfellows', 'playfully', 'playing', 'playmate', 'plays', 'plaything', 'plead', 'pleasant', 'please', 'pleased', 'pleases', 'pleasing', 'pleasurable', 'pleasure', 'pleasures', 'pledge', 'plentiful', 'plenty', 'plot', 'plunge', 'plunged', 'plutarch', 'plutarch’s', 'pocket', 'poems', 'poet', 'poetry', 'poets', 'poignant', 'poignantly', 'point', 'pointed', 'pointing', 'points', 'poison', 'poisoned', 'pole', 'politic', 'politics', 'polluted', 'pollutes', 'pool', 'poor', 'popular', 'population', 'populous', 'pore', 'port', 'portend', 'porter', 'portion', 'portmanteau', 'portrait', 'position', 'positively', 'possess', 'possessed', 'possesses', 'possessing', 'possession', 'possessions', 'possibility', 'possible', 'possibly', 'post', 'posterity', 'postpone', 'postponed', 'posture', 'potent', 'pour', 'poured', 'pouring', 'pours', 'poverty', 'power', 'powerful', 'powers', 'practical', 'practically', 'practice', 'praise', 'praised', 'praises', 'prayed', 'prayer', 'prayers', 'precarious', 'precaution', 'precautions', 'preceded', 'preceding', 'preceptors', 'precepts', 'precious', 'precipice', 'precipices', 'precipitate', 'precipitated', 'precipitation', 'precipitous', 'precisely', 'precision', 'predilection', 'preference', 'preferred', 'prejudice', 'prejudiced', 'prejudices', 'preliminary', 'prelude', 'preparation', 'preparations', 'preparatory', 'prepare', 'prepared', 'preparing', 'prepossess', 'prescribed', 'presence', 'present', 'presented', 'presentiment', 'presenting', 'presently', 'presents', 'preservation', 'preserve', 'preserved', 'preserver', 'preside', 'press', 'pressed', 'presumption', 'pretence', 'pretend', 'pretended', 'pretension', 'pretty', 'prevail', 'prevailed', 'prevent', 'prevented', 'prevents', 'previous', 'previously', 'prey', 'preyed', 'price', 'pride', 'priest', 'principal', 'principally', 'principle', 'principles', 'print', 'prison', 'prisoner', 'private', 'prize', 'prized', 'probabilities', 'probability', 'probable', 'probably', 'proceed', 'proceeded', 'proceeding', 'proceedings', 'process', 'proclaim', 'procrastinate', 'procure', 'procured', 'produce', 'produced', 'produces', 'production', 'productions', 'profane', 'profession', 'professional', 'professions', 'professor', 'professors', 'professor’s', 'proficiency', 'profited', 'profits', 'profound', 'profoundly', 'profundity', 'progeny', 'prognosticate', 'prognosticated', 'progress', 'progressively', 'project', 'projectors', 'projects', 'prolong', 'prolonged', 'prolonging', 'prometheus', 'promise', 'promised', 'promises', 'promising', 'promontory', 'pronounce', 'pronounced', 'pronouncing', 'pronunciation', 'proof', 'propagated', 'proper', 'properties', 'property', 'prophesied', 'prophetic', 'proportion', 'proportionably', 'proportionate', 'proportions', 'propose', 'proposed', 'proposition', 'prosecution', 'prospect', 'prospects', 'prosperity', 'prosperous', 'protect', 'protecting', 'protection', 'protector', 'protectors', 'protectress', 'protestations', 'protracted', 'protraction', 'proud', 'prove', 'proved', 'proves', 'provide', 'provided', 'providence', 'provision', 'provisions', 'provocation', 'provoke', 'prudence', 'prudent', 'public', 'publicly', 'pulled', 'pulling', 'pulpit', 'pulse', 'pulses', 'punish', 'punishment', 'pupil', 'purchase', 'purchasing', 'pure', 'purest', 'purloined', 'purport', 'purpose', 'purposed', 'purposes', 'pursue', 'pursued', 'pursues', 'pursuing', 'pursuit', 'pursuits', 'push', 'put', 'putting', 'puzzled', 'pyramids', 'qualities', 'quality', 'quantity', 'quarter', 'quarters', 'queen', 'quelling', 'quenched', 'question', 'questioned', 'questions', 'quick', 'quickly', 'quiet', 'quieted', 'quietly', 'quit', 'quite', 'quitted', 'quitting', 'quiver', 'quivered', 'quivering', 'r', 'race', 'radiance', 'radiant', 'raft', 'rage', 'ragged', 'raging', 'rain', 'raise', 'raised', 'raises', 'raising', 'ramble', 'rambled', 'rambles', 'rambling', 'ran', 'rang', 'range', 'ranged', 'ranging', 'rank', 'ranked', 'rankle', 'rankling', 'rapid', 'rapidity', 'rapidly', 'rapture', 'rapturously', 'rare', 'rarely', 'rash', 'rashly', 'rate', 'rather', 'rational', 'raved', 'raven', 'ravenous', 'ravine', 'ravines', 'ravings', 'ravish', 'ravished', 'rawness', 'rays', 're', 'reach', 'reached', 'read', 'readier', 'reading', 'ready', 'real', 'realise', 'realised', 'realities', 'reality', 'really', 'reap', 'reason', 'reasonable', 'reasonably', 'reasoned', 'reasoning', 'reasons', 'reassure', 'reassured', 'recall', 'recalled', 'recapitulation', 'receive', 'received', 'receiving', 'recent', 'receptacle', 'reception', 'recess', 'recesses', 'recital', 'recognise', 'recognised', 'recollect', 'recollected', 'recollection', 'recollections', 'recommence', 'recommencing', 'recommended', 'recompense', 'recompensing', 'reconcile', 'reconciled', 'record', 'recorded', 'recording', 'recourse', 'recover', 'recovered', 'recovering', 'recovery', 'recur', 'recurred', 'recurrence', 'red', 'redeem', 'redress', 'reduced', 'reference', 'referred', 'refined', 'refinement', 'reflect', 'reflected', 'reflecting', 'reflection', 'reflections', 'reflects', 'refrain', 'refrained', 'refreshed', 'refuge', 'refuse', 'refused', 'refusing', 'regard', 'regarded', 'regarding', 'regards', 'region', 'regions', 'regret', 'regretted', 'regular', 'regularity', 'regularly', 'regulate', 'regulated', 'reign', 'reigned', 'reiterating', 'rejected', 'rejoice', 'rejoiced', 'rejoined', 'rekindled', 'relapse', 'relapses', 'relate', 'related', 'relates', 'relating', 'relation', 'relations', 'relationships', 'relative', 'relatives', 'relaxed', 'release', 'released', 'relics', 'relied', 'relief', 'relieve', 'relieved', 'religion', 'religions', 'relinquish', 'relinquished', 'relinquishing', 'reluctant', 'rely', 'remain', 'remainder', 'remained', 'remaining', 'remains', 'remark', 'remarkable', 'remarkably', 'remarked', 'remedy', 'remember', 'remembered', 'remembering', 'remembrance', 'remembrancers', 'remind', 'reminded', 'reminds', 'remissness', 'remnants', 'remonstrate', 'remorse', 'remote', 'remoter', 'remotest', 'removal', 'remove', 'removed', 'removes', 'render', 'rendered', 'rendering', 'renders', 'rendezvous', 'rending', 'rends', 'renew', 'renewed', 'renewing', 'renounce', 'renovating', 'renowned', 'rent', 'repaid', 'repair', 'repaired', 'repairing', 'repassed', 'repast', 'repay', 'repeat', 'repeated', 'repeating', 'repent', 'repentance', 'repentant', 'repetition', 'repined', 'replace', 'replaced', 'replenished', 'replete', 'replied', 'reply', 'report', 'reported', 'repose', 'reposed', 'representations', 'represented', 'repressed', 'reproach', 'reproaches', 'reprobated', 'reproduce', 'republic', 'republican', 'republics', 'repugnance', 'repulses', 'repulsive', 'reputation', 'request', 'requested', 'require', 'required', 'requires', 'requisite', 'requisition', 'requited', 'reread', 'rescued', 'research', 'resemblance', 'resembled', 'resembling', 'resentment', 'reserve', 'reserved', 'reside', 'resided', 'residence', 'residents', 'residing', 'resign', 'resignation', 'resigned', 'resist', 'resistless', 'resolution', 'resolutions', 'resolve', 'resolved', 'resolving', 'resource', 'resources', 'respect', 'respectable', 'respected', 'respecting', 'respects', 'respite', 'rest', 'rested', 'resting', 'restless', 'restlessness', 'restoration', 'restorative', 'restore', 'restored', 'restrain', 'restrained', 'rests', 'result', 'results', 'resume', 'resumed', 'retain', 'retains', 'retard', 'retarded', 'retire', 'retired', 'retirement', 'retreat', 'retreated', 'retreats', 'retribution', 'retrod', 'retrospect', 'return', 'returned', 'returning', 'returns', 'reuss', 'reveal', 'revealed', 'revel', 'revenge', 'reverberated', 'reverence', 'reverential', 'reverie', 'reveries', 'reverse', 'reverses', 'reverted', 'revisit', 'revive', 'revived', 'revoke', 'revolt', 'revolution', 'revolutions', 'revolved', 'reward', 'rewarded', 'rhine', 'rhone', 'ribbons', 'rich', 'riches', 'ridges', 'ridicule', 'riding', 'rifts', 'right', 'riot', 'ripen', 'rippling', 'rise', 'risen', 'rising', 'rival', 'river', 'rivers', 'road', 'roads', 'roaming', 'roared', 'roarings', 'roasted', 'rob', 'robbed', 'robert', 'rock', 'rocks', 'rocky', 'roll', 'rolled', 'roman', 'romance', 'romans', 'romantic', 'rome', 'romulus', 'roncesvalles', 'roof', 'room', 'rooms', 'rooted', 'roots', 'rose', 'roses', 'rosy', 'rotterdam', 'rough', 'rougher', 'roughly', 'round', 'rouse', 'roused', 'rouses', 'route', 'routine', 'row', 'rowing', 'rubbed', 'rubbing', 'rudder', 'rude', 'ruffled', 'rugged', 'ruggedness', 'ruin', 'ruined', 'ruins', 'rule', 'ruled', 'rumbling', 'run', 'running', 'rush', 'rushed', 'rushing', 'russia', 'russian', 'rustic', 'rustling', 'sacred', 'sacrifice', 'sacrificed', 'sacrilege', 'sad', 'saddest', 'sadness', 'safe', 'safety', 'safie', 'sagacity', 'said', 'sail', 'sailed', 'sailing', 'sailors', 'sails', 'saintly', 'sake', 'sakes', 'sal', 'sallies', 'salubrious', 'salutations', 'saluted', 'salvation', 'same', 'sands', 'sandy', 'sang', 'sanguinary', 'sank', 'sanskrit', 'sar', 'sat', 'satan', 'satiate', 'satiated', 'satisfaction', 'satisfied', 'satisfy', 'satisfying', 'savage', 'save', 'saved', 'saville', 'saviour', 'savoury', 'savoy', 'saw', 'say', 'saying', 'says', 'scaffold', 'scale', 'scaling', 'scanty', 'scarce', 'scarcely', 'scared', 'scaring', 'scarlet', 'scattered', 'scene', 'scenery', 'scenes', 'scent', 'scents', 'schemes', 'schiavi', 'school', 'schoolboys', 'schoolfellow', 'schoolmaster', 'schools', 'science', 'sciences', 'scientific', 'scion', 'scoffing', 'scope', 'scorn', 'scotch', 'scotland', 'scourge', 'scraggy', 'scream', 'screamed', 'sea', 'seafaring', 'seal', 'sealed', 'seamen', 'search', 'searching', 'seas', 'seashore', 'season', 'seasons', 'seat', 'seated', 'seating', 'secheron', 'secluded', 'seclusion', 'second', 'secondary', 'secret', 'secretly', 'secrets', 'secure', 'secured', 'securely', 'securing', 'security', 'sedulous', 'see', 'seeing', 'seek', 'seeking', 'seem', 'seemed', 'seeming', 'seemingly', 'seems', 'seen', 'seize', 'seized', 'seizing', 'seizure', 'seldom', 'select', 'selected', 'self', 'selfish', 'selfishness', 'sell', 'semblance', 'send', 'sending', 'sensation', 'sensations', 'sense', 'senseless', 'senses', 'sensibilities', 'sensibility', 'sensibly', 'sensitive', 'sensitiveness', 'sent', 'sentence', 'sentences', 'sentiment', 'sentiments', 'separated', 'separation', 'september', 'sepulchre', 'serene', 'serenity', 'series', 'serious', 'seriousness', 'serpent', 'servant', 'servants', 'serve', 'serves', 'service', 'serviceable', 'services', 'serving', 'servox', 'set', 'setting', 'settled', 'seven', 'seventeen', 'several', 'severe', 'severity', 'sex', 'sexes', 'shade', 'shaded', 'shades', 'shadow', 'shadows', 'shake', 'shaken', 'shakespeare', 'shall', 'shame', 'shamefully', 'shape', 'shapes', 'share', 'shared', 'shattered', 'she', 'shed', 'sheet', 'sheets', 'shelley', 'shells', 'shelter', 'sheltered', 'shepherd', 'shepherd’s', 'shifting', 'shine', 'shining', 'ship', 'shipping', 'shiver', 'shivering', 'shock', 'shocking', 'shocks', 'shone', 'shook', 'shooting', 'shore', 'shores', 'short', 'shortened', 'shortly', 'shot', 'should', 'shoulder', 'shoulders', 'shout', 'show', 'showed', 'shower', 'showers', 'shown', 'shrank', 'shrieked', 'shrieks', 'shrill', 'shrine', 'shrink', 'shrivelled', 'shroud', 'shudder', 'shuddered', 'shuddering', 'shunned', 'shut', 'shutters', 'shutting', 'sick', 'sickbed', 'sicken', 'sickened', 'sickening', 'sickness', 'side', 'sides', 'sigh', 'sighed', 'sight', 'sights', 'sign', 'signal', 'signification', 'signs', 'silence', 'silent', 'silken', 'silver', 'similar', 'similarity', 'simple', 'simpler', 'simplest', 'simply', 'since', 'sincere', 'sincerely', 'sincerest', 'sincerity', 'single', 'singular', 'singularly', 'sinister', 'sink', 'sinking', 'sinks', 'sinned', 'sins', 'sir', 'siroc', 'sister', 'sit', 'sitting', 'situated', 'situation', 'situations', 'six', 'sixteen', 'sixth', 'skeleton', 'skies', 'skiff', 'skill', 'skims', 'skin', 'skirted', 'skirting', 'sky', 'slackened', 'slaked', 'slaughter', 'slave', 'slavery', 'sledge', 'sledges', 'sleep', 'sleeper', 'sleeping', 'sleepless', 'sleeps', 'slenderly', 'slept', 'slight', 'slightest', 'slipped', 'sloping', 'slothful', 'slough', 'slow', 'slowly', 'slumbers', 'sly', 'small', 'smelt', 'smile', 'smiled', 'smiles', 'smiling', 'smitten', 'smoke', 'smooth', 'smoothed', 'smothered', 'snake', 'snatched', 'snatches', 'snow', 'snows', 'snowy', 'so', 'soar', 'soaring', 'sobbed', 'sobs', 'social', 'society', 'sockets', 'sod', 'soft', 'soften', 'softened', 'softly', 'softness', 'soil', 'soldier', 'sole', 'solely', 'solemn', 'solemnisation', 'solemnising', 'solemnity', 'solicited', 'solicitude', 'solid', 'solitary', 'solitude', 'solitudes', 'solon', 'solve', 'sombre', 'some', 'someone', 'something', 'sometimes', 'somewhat', 'son', 'song', 'songs', 'son’s', 'soon', 'sooner', 'soothe', 'soothed', 'soothing', 'sophisms', 'sorrow', 'sorrowful', 'sorrowing', 'sorrows', 'sorry', 'sought', 'soul', 'souls', 'sound', 'sounded', 'sounding', 'soundly', 'sounds', 'soup', 'source', 'sources', 'south', 'southern', 'southwards', 'southwesterly', 'space', 'spanish', 'spare', 'spared', 'spark', 'sparkled', 'sparrow', 'speak', 'speaker', 'speaking', 'speaks', 'species', 'specimen', 'speck', 'specked', 'spectacle', 'spectators', 'spectre', 'speculation', 'speculations', 'speech', 'speechless', 'speed', 'speedily', 'speedy', 'spend', 'spent', 'sphere', 'spire', 'spires', 'spirit', 'spirits', 'spite', 'splendour', 'splintered', 'split', 'spoiled', 'spoiler', 'spoke', 'spoken', 'sport', 'sportiveness', 'spot', 'spots', 'spout', 'sprang', 'spread', 'spreading', 'spring', 'springing', 'springs', 'sprung', 'spurn', 'spurned', 'spurred', 'squalid', 'squalidness', 'squat', 'st', 'stag', 'stage', 'stagecoach', 'stages', 'staggered', 'staircase', 'stairs', 'stamp', 'stand', 'standard', 'standing', 'star', 'stare', 'stared', 'starry', 'stars', 'started', 'starting', 'startled', 'starvation', 'state', 'stated', 'stately', 'statement', 'states', 'station', 'stature', 'stay', 'stayed', 'steadily', 'steady', 'steal', 'stealth', 'steel', 'steep', 'steeple', 'steeples', 'steered', 'step', 'stepped', 'steps', 'stick', 'stiff', 'stifle', 'stigma', 'still', 'stillness', 'stimulated', 'stimulus', 'sting', 'stings', 'stir', 'stirred', 'stock', 'stole', 'stolen', 'stone', 'stones', 'stony', 'stood', 'stop', 'stopped', 'stopping', 'store', 'stores', 'storm', 'story', 'stove', 'straight', 'strain', 'strained', 'strange', 'strangely', 'stranger', 'strangers', 'stranger’s', 'strangest', 'strangled', 'strasburgh', 'straw', 'stream', 'streamed', 'streams', 'street', 'streets', 'strength', 'strengthened', 'strenuously', 'stretch', 'stretched', 'strewed', 'strife', 'strive', 'striving', 'strong', 'stronger', 'strongly', 'strove', 'struck', 'structure', 'struggle', 'struggled', 'student', 'students', 'student’s', 'studied', 'studies', 'study', 'studying', 'stuff', 'stump', 'stupendous', 'stupid', 'sty', 'style', 'subdue', 'subdued', 'subduing', 'subject', 'subjects', 'sublime', 'submission', 'submit', 'subscribed', 'subsequent', 'subsist', 'subsisted', 'subsistence', 'substance', 'succeed', 'succeeded', 'success', 'successfully', 'succession', 'successive', 'successors', 'succour', 'such', 'sudden', 'suddenly', 'suffer', 'suffered', 'sufferer', 'suffering', 'sufferings', 'suffice', 'sufficiency', 'sufficient', 'sufficiently', 'suffocated', 'suggested', 'suggestion', 'suicide', 'suit', 'suited', 'sullen', 'sum', 'summer', 'summers', 'summit', 'summits', 'summoned', 'sun', 'sunday', 'sunk', 'sunlight', 'sunny', 'sunrise', 'sunset', 'sunshine', 'superfluous', 'superhuman', 'superior', 'superiors', 'supernatural', 'superscription', 'superstition', 'supple', 'suppliant', 'supplication', 'supplied', 'supply', 'support', 'supported', 'suppose', 'supposed', 'supposing', 'supposition', 'suppress', 'suppressed', 'suppressing', 'supreme', 'sure', 'surely', 'surface', 'surgeon', 'surmount', 'surmounted', 'surmounting', 'surpassed', 'surpassing', 'surprise', 'surprised', 'surprising', 'surround', 'surrounded', 'surrounding', 'survive', 'surviving', 'survivors', 'susceptible', 'suspect', 'suspended', 'suspense', 'suspicion', 'suspicions', 'suspicious', 'sustain', 'sustained', 'sustenance', 'swallow', 'swallowed', 'sway', 'swear', 'sweet', 'sweeter', 'sweetest', 'sweetness', 'swell', 'swelled', 'swelling', 'swells', 'swept', 'swifter', 'swiftness', 'swim', 'swimming', 'swiss', 'switzerland', 'sword', 'swore', 'sworn', 'symmetry', 'sympathies', 'sympathise', 'sympathised', 'sympathising', 'sympathy', 'symptoms', 'syndic', 'syndics', 'system', 'systems', 't', 'table', 'tackle', 'tainted', 'take', 'taken', 'takes', 'taking', 'tale', 'talent', 'talents', 'tales', 'talk', 'talked', 'talking', 'talks', 'tall', 'tamer', 'tangible', 'tapers', 'tapped', 'tardily', 'tarnish', 'tartary', 'task', 'taste', 'tasted', 'tastes', 'taught', 'taunt', 'tavernier', 'tay', 'teach', 'teacher', 'teachers', 'tear', 'tearful', 'tearing', 'tears', 'teased', 'tedious', 'teeth', 'telescopes', 'tell', 'temper', 'temperature', 'tempest', 'temple', 'temples', 'temporary', 'temptation', 'tempted', 'ten', 'tend', 'tended', 'tendency', 'tender', 'tenderest', 'tenderly', 'tenderness', 'tenement', 'tenets', 'tenfold', 'tenth', 'term', 'terminate', 'terminated', 'termination', 'terms', 'terrible', 'terribly', 'terrific', 'terrifically', 'terrified', 'terror', 'terrors', 'tertiary', 'testify', 'testimonies', 'testimony', 'texture', 'thames', 'than', 'thank', 'thanked', 'thankfulness', 'thanks', 'that', 'thatch', 'that’s', 'the', 'thee', 'their', 'theirs', 'them', 'theme', 'themselves', 'then', 'thence', 'thenceforth', 'theories', 'theory', 'there', 'therefore', 'these', 'theseus', 'they', 'thick', 'thickened', 'thickly', 'thin', 'thine', 'thing', 'things', 'think', 'thinking', 'thinks', 'thinner', 'third', 'thirst', 'thirsted', 'thirsting', 'thirteen', 'this', 'thither', 'thomas’', 'thonon', 'those', 'thou', 'thought', 'thoughtful', 'thoughtfulness', 'thoughtlessly', 'thoughts', 'thousand', 'thousands', 'thousandth', 'threat', 'threaten', 'threatened', 'threatening', 'threats', 'three', 'threshold', 'threw', 'thrice', 'thrill', 'throat', 'throats', 'throbbings', 'through', 'throw', 'throwing', 'thrown', 'thrush', 'thrust', 'thunder', 'thunders', 'thunderstorm', 'thursday', 'thus', 'thy', 'thyself', 'tide', 'tidings', 'tie', 'ties', 'tilbury', 'till', 'time', 'times', 'timid', 'timorous', 'tinged', 'tingle', 'tingling', 'tintern', 'title', 'to', 'today', 'together', 'toil', 'toiled', 'toils', 'toilsome', 'tokens', 'told', 'tolerable', 'tolerably', 'tolerated', 'tomb', 'tomorrow', 'tone', 'toned', 'tones', 'tongue', 'tongues', 'too', 'took', 'tools', 'top', 'topic', 'torch', 'torches', 'tore', 'torment', 'tormented', 'tormenting', 'tormentor', 'torments', 'torn', 'torpor', 'torrent', 'torrents', 'torture', 'tortured', 'torturer', 'tortures', 'torturing', 'total', 'totally', 'touch', 'touched', 'touching', 'tour', 'toward', 'towards', 'tower', 'towered', 'towering', 'towers', 'town', 'towns', 'trace', 'traced', 'traces', 'tracing', 'track', 'trade', 'trader', 'tragedy', 'train', 'trained', 'trains', 'trait', 'traitor', 'trample', 'trampled', 'trance', 'tranquil', 'tranquillise', 'tranquillised', 'tranquillity', 'tranquilly', 'transacted', 'transaction', 'transcendent', 'transfer', 'transitory', 'transmit', 'transmuted', 'transparent', 'transport', 'transported', 'transversely', 'trash', 'travel', 'travelled', 'traveller', 'travellers', 'traveller’s', 'travelling', 'travels', 'traverse', 'traversed', 'traversing', 'treacherous', 'treachery', 'tread', 'treading', 'treasure', 'treasures', 'treated', 'treating', 'treatment', 'treble', 'tree', 'trees', 'tremble', 'trembled', 'trembling', 'tremendous', 'tremulous', 'trial', 'trials', 'tribute', 'trickle', 'trickling', 'tried', 'trifled', 'trifling', 'triumph', 'triumphant', 'triumphantly', 'triumphed', 'trod', 'trouble', 'troubled', 'truce', 'true', 'truest', 'truly', 'trust', 'truth', 'try', 'tumult', 'tumultuous', 'turbulence', 'turk', 'turkey', 'turkish', 'turks', 'turmoil', 'turn', 'turned', 'turning', 'turnkeys', 'turns', 'tutored', 'twelve', 'twenty', 'twice', 'twinkling', 'two', 'type', 'tyrannical', 'tyranny', 'tyrant', 'tyrants', 'tyros', 'ugliness', 'ugly', 'ultimately', 'unabated', 'unable', 'unaccountable', 'unacquainted', 'unadept', 'unallied', 'unalterable', 'unavoidable', 'unbelief', 'unbending', 'unborrow’d', 'unbounded', 'unbridled', 'unceasing', 'uncertain', 'unchained', 'unchecked', 'uncle', 'uncle’s', 'uncommon', 'uncommonly', 'unconscious', 'uncontrollable', 'uncontrollably', 'uncouth', 'uncovered', 'undeceive', 'undeceiving', 'under', 'undergo', 'undergone', 'understand', 'understanding', 'understood', 'undertake', 'undertaking', 'underwent', 'underwood', 'undiscovered', 'undisturbed', 'undivided', 'undoubtedly', 'undulations', 'unearthly', 'uneasiness', 'uneasy', 'uneducated', 'unemployed', 'unequal', 'unequalled', 'uneven', 'unexampled', 'unexpected', 'unexplored', 'unfailing', 'unfair', 'unfashioned', 'unfavourable', 'unfeeling', 'unfinished', 'unfit', 'unfitness', 'unfitted', 'unfold', 'unfolded', 'unfolding', 'unformed', 'unfortunate', 'unfortunately', 'unfulfilled', 'ungazed', 'ungratitude', 'unguarded', 'unhallowed', 'unhappiness', 'unhappy', 'unheard', 'uniform', 'unintelligible', 'uninterested', 'uninteresting', 'uninterrupted', 'union', 'unite', 'united', 'universal', 'university', 'unjust', 'unjustly', 'unkindness', 'unknown', 'unlawful', 'unless', 'unlike', 'unlimited', 'unlocked', 'unmingled', 'unmolested', 'unnatural', 'unobserving', 'unparalleled', 'unperceived', 'unplastered', 'unpractised', 'unprejudiced', 'unprotected', 'unqualified', 'unquenched', 'unquiet', 'unravel', 'unrelaxed', 'unremitted', 'unremitting', 'unreservedly', 'unrestrained', 'unsatisfactory', 'unsatisfied', 'unseen', 'unsettled', 'unsocial', 'unsoftened', 'unspeakable', 'unstained', 'unsuccessful', 'unsullied', 'unsupported', 'unsympathised', 'untamed', 'untaught', 'until', 'untimely', 'untrodden', 'unusual', 'unutterable', 'unveiled', 'unvisited', 'unwearied', 'unwholesome', 'unwilling', 'unwillingly', 'unwillingness', 'unworthiness', 'unworthy', 'up', 'upon', 'upright', 'urged', 'uri', 'us', 'usage', 'use', 'used', 'useful', 'usefulness', 'useless', 'uses', 'using', 'usual', 'usually', 'utensils', 'utility', 'utmost', 'utter', 'utterance', 'uttered', 'uttering', 'utterly', 'vacancy', 'vacant', 'vacillating', 'vagabond', 'vagrants', 'vain', 'vainly', 'valais', 'vale', 'vales', 'valley', 'valleys', 'valuable', 'value', 'valued', 'vampire', 'vanish', 'vanished', 'vanquished', 'variable', 'varied', 'variegated', 'variety', 'various', 'vast', 'vaud', 'vaults', 've', 'vegetables', 'vehement', 'vehicle', 'veil', 'veiled', 'veins', 'venerable', 'vengeance', 'venom', 'vent', 'venting', 'venture', 'ventured', 'ventures', 'verdant', 'verdure', 'verge', 'very', 'vessel', 'vessels', 'vestige', 'vexations', 'viands', 'vicar', 'vice', 'vices', 'vicinity', 'vicious', 'victim', 'victims', 'victor', 'victorious', 'victory', 'view', 'viewed', 'views', 'vigilance', 'vigorous', 'vigour', 'vile', 'villa', 'village', 'villagers', 'villain', 'villains', 'vines', 'vineyards', 'vintage', 'violence', 'violent', 'violently', 'virtue', 'virtues', 'virtuous', 'visage', 'visible', 'vision', 'visions', 'visit', 'visited', 'visitings', 'visitor', 'visits', 'vital', 'vivacity', 'vivid', 'voice', 'voiceless', 'voices', 'void', 'volcano', 'volney’s', 'volume', 'volumes', 'voluntarily', 'voluntary', 'vow', 'vowed', 'vows', 'voyage', 'voyages', 'vulgar', 'vulture', 'w', 'wafted', 'wail', 'wait', 'waited', 'waiting', 'wakefield', 'waking', 'waldman', 'walk', 'walked', 'walking', 'walks', 'wall', 'wallet', 'walls', 'walton', 'wan', 'wander', 'wandered', 'wanderer', 'wandering', 'wanderings', 'wand’ring', 'want', 'wantonly', 'wantonness', 'wants', 'war', 'warbling', 'warm', 'warmed', 'warmer', 'warmest', 'warmly', 'warmth', 'warrant', 'warring', 'wars', 'was', 'waste', 'wasted', 'wasting', 'watch', 'watched', 'watchful', 'watching', 'water', 'waterfalls', 'waters', 'watery', 'waved', 'wavering', 'waves', 'way', 'ways', 'we', 'weak', 'weaken', 'weakened', 'weakness', 'wealth', 'wean', 'weapons', 'wear', 'wearied', 'wearily', 'wearing', 'wears', 'weary', 'wearying', 'weather', 'wedding', 'week', 'weeks', 'weep', 'weeping', 'weeps', 'weigh', 'weighed', 'weighs', 'weight', 'welcome', 'welcomed', 'welfare', 'well', 'went', 'wept', 'were', 'wert', 'werter', 'werter’s', 'west', 'western', 'westmorland', 'wet', 'whale', 'whaler', 'what', 'whatever', 'whatsoever', 'wheel', 'when', 'whence', 'whenever', 'where', 'wherefore', 'wherever', 'whether', 'which', 'while', 'whilst', 'whine', 'whirled', 'whirlwind', 'whirlwinds', 'whisper', 'whispered', 'whispers', 'white', 'whiteness', 'whitewashed', 'whither', 'who', 'whole', 'wholesome', 'wholly', 'whom', 'whose', 'why', 'wicked', 'wickedness', 'wide', 'wider', 'widow', 'width', 'wife', 'wild', 'wildest', 'wildness', 'wilds', 'wiliness', 'will', 'william', 'willingly', 'willow', 'willowy', 'wilt', 'win', 'wind', 'winding', 'windings', 'window', 'windows', 'winds', 'windsor', 'wine', 'winged', 'wings', 'winning', 'winter', 'wipe', 'wiped', 'wiping', 'wisdom', 'wise', 'wiser', 'wisest', 'wish', 'wished', 'wishes', 'wishing', 'with', 'withdrawn', 'withdrew', 'withered', 'withhold', 'within', 'without', 'withstand', 'witness', 'witnessed', 'witnesses', 'wives', 'woe', 'woeful', 'woes', 'wollstonecraft', 'woman', 'woman’s', 'women', 'won', 'wonder', 'wonderful', 'wonderfully', 'wonders', 'wondrous', 'wondrously', 'wont', 'wood', 'woods', 'woolwich', 'word', 'words', 'wordsworth’s', 'wore', 'work', 'worked', 'working', 'workman', 'works', 'workshop', 'world', 'worldly', 'worm', 'worms', 'worn', 'worse', 'worship', 'worst', 'worth', 'worthy', 'would', 'wouldst', 'wound', 'wounded', 'wounds', 'wrap', 'wrapped', 'wrapping', 'wreak', 'wreaked', 'wreaths', 'wreck', 'wrecked', 'wrenched', 'wrestle', 'wretch', 'wretched', 'wretchedly', 'wretchedness', 'wrinkled', 'write', 'writers', 'writes', 'writhed', 'writhing', 'writing', 'writings', 'written', 'wrong', 'wrongfully', 'wrote', 'wrought', 'wrung', 'yard', 'yards', 'ye', 'year', 'yearned', 'years', 'yellow', 'yes', 'yesterday', 'yesternight’s', 'yet', 'yield', 'yielded', 'yon', 'you', 'young', 'younger', 'youngest', 'youngster', 'your', 'yours', 'yourself', 'yourselves', 'youth', 'youthful', 'zeal', '’']\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Raw Strings**\n",
        "There's a small issue when a regular expression pattern contains any special 'commands' (called escape or control sequences). We have already been using escape sequences -- the `'\\n'` is one of those special characters that is replaced with a newline when it appears in a string. To tell Python NOT to ignore any control sequences, you need to preface the string with an `r` -- which means a *raw* string. You can see how this will affect the string evaluation in the following:\n"
      ],
      "metadata": {
        "id": "4PBmB9tyZ3vl"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "VB6mWnk7PS3y",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "c106a302-0a32-4e2e-904f-98fb17ed840d"
      },
      "source": [
        "print( \"Hello\\nWorld\\n\", end='')\n",
        "print(r\"Hello\\nWorld\\n\", end='')"
      ],
      "execution_count": 15,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Hello\n",
            "World\n",
            "Hello\\nWorld\\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "In the second print statement, the `\\n` is printed as opposed to being interpreted to force a return or linefeed.\n",
        "\n",
        "You can use the same raw string to print out unicode characters. We will discuss unicode in another lesson. But you can think of it as a way to provide a representation of all possible characters. Unicode provides a unique number for every character, no matter what the platform, no matter what the program, no matter what the language. We'll learn more on unicode later."
      ],
      "metadata": {
        "id": "riRDGBeMkXdX"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "nNKK3XG_PS34",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "55f2e8fe-174c-4f1d-99cc-2f748b51f71f"
      },
      "source": [
        "print( \"Hello\\nWorld\\n\", end='')\n",
        "print(r'\\U0001f441\\U00002764\\U0000FE0F\\U0001f40d')\n",
        "print('\\U0001f441\\U00002764\\U0000FE0F\\U0001f40d')"
      ],
      "execution_count": 16,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Hello\n",
            "World\n",
            "\\U0001f441\\U00002764\\U0000FE0F\\U0001f40d\n",
            "👁❤️🐍\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Once again, you should know how the above two statements are treated differently by prefacing one of the strings with `r`.\n",
        "\n",
        "With regular expression we ALWAYS use raw strings.\n",
        "```\n",
        "pattern = r'[\\'0-9A-Za-z]+'\n",
        "```"
      ],
      "metadata": {
        "id": "-aLr8n2GkblV"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Back to Books with Frankenstein**\n",
        "At this point, we need to inspect the tokens and decide if we are getting the right values.\n",
        "\n",
        "For example, back to line 80 in Frankenstein, we can see this:\n",
        "\n",
        "> *Six years have passed since I resolved on my present undertaking. I\n",
        "can, even now, remember the hour from which I dedicated myself to this\n",
        "great enterprise. I commenced by inuring my body to hardship. I\n",
        "accompanied the whale-fishers on several expeditions to the North Sea;\n",
        "I voluntarily endured cold, famine, thirst, and want of sleep; I often\n",
        "worked harder than the common sailors during the day and devoted my\n",
        "nights to the study of mathematics, the theory of medicine, and those\n",
        "branches of physical science from which a naval adventurer might derive\n",
        "the greatest practical advantage. Twice I actually hired myself as an\n",
        "under-mate in a Greenland whaler, and acquitted myself to admiration. I\n",
        "must own I felt a little proud when my captain offered me the second\n",
        "dignity in the vessel and entreated me to remain with the greatest\n",
        "earnestness, so valuable did he consider my services.*\n"
      ],
      "metadata": {
        "id": "kkS4P8nRcSgd"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "For this specific book, any word with a hyphen (e.g. `whale-fishers`) would be\n",
        "splited into two because we didn't include the hyphen in the regular expression. The issue is that in our pattern we are *excluding* words with this single hyphen in them.\n",
        "\n",
        "Let's find them using the following pattern on the whole book:"
      ],
      "metadata": {
        "id": "GQq0R4P9THtx"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "MJ6eelQ7PS36",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "ed1a8ece-d5de-4f2e-e662-243a35d2b7d3"
      },
      "source": [
        "pattern = r\"['A-Za-z0-9]+[-]['A-Za-z0-9]+\"\n",
        "print(len(regex_find_words(BOOK_TEXT, pattern)))\n",
        "print(set(regex_find_words(BOOK_TEXT, pattern)))"
      ],
      "execution_count": 17,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "121\n",
            "{'self-interest', 'half-clothed', 'heart-rending', 'unheard-of', 'brother-in', 'ten-thousandth', 'grave-worms', 'heart-moving', 'cabin-window', 'ill-fated', 'market-woman', 'soul-subduing', 'self-taught', 'self-violence', 'whale-fishers', 'mole-hills', 'milk-house', 'fellow-pupil', 'star-light', 'late-discovered', 'mantel-piece', 'self-reproaches', 'heart-felt', 'half-suppressed', 'self-devoted', 'soul-inspiriting', 'slaughter-house', 'fiend-like', 'land-sledge', 'joy-imparting', 'country-man', 'shrine-dedicated', 'ever-moving', 'under-mate', 'half-finished', 'ill-suited', 'snow-clad', 'stag-like', 'half-painful', 'prize-money', 'heart-sickening', 'mountain-top', 'arch-enemy', 'full-toned', 'ever-gentle', 'lap-dog', 'twenty-eight', 'bed-chamber', 'ever-varied', 'hiding-places', 'ice-rock', 'narrow-minded', 'would-be', 'fellow-creatures', 'fishing-boat', 'self-sacrifice', 'long-continued', 'thrice-accursed', 'book-keeping', 'horror-struck', 'much-loved', 'Fairy-land', 'ever-changing', 'death-warrant', 'death-knell', 'frank-hearted', 'self-control', 'rain-dropping', 'never-dying', 'hiding-place', 'mountain-stream', 'worldly-minded', 'water-spout', 'post-road', 'well-known', 'wedding-night', 'half-extinguished', 'long-lost', 'sure-footed', 'sea-room', 'dwelling-places', 'dark-leaved', 'self-deceit', 'Havre-de', 'never-ending', 'resting-place', 'school-fellows', 'never-failing', 'self-satisfaction', 'self-accusations', 'ice-caves', 're-echoed', 'ice-rifts', 'ever-watchful', 'self-educated', 'ill-looking', 'heart-broken', 'whale-fishing', 'dark-eyed', 'heaven-sent', 'self-command', 'charnel-houses', 'dun-white', 'well-being', 'presence-chamber', 'arch-fiend'}\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "\n",
        "This finds all the words that have a SINGLE hyphen `[-]` with at least one letter before it and at least one letter after it. There are 121 such words in our book. Finding them without using regular expressions would be very tedious.\n",
        "\n",
        "We also can make that single hyphen optional by using the `?` (a special character that means 0 or 1 of the previous pattern)."
      ],
      "metadata": {
        "id": "mR5O1wRtlTNF"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "uRGKj6huPS38",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "49d117f9-7467-4159-bacc-e274579aaf2a"
      },
      "source": [
        "pattern = r\"['0-9A-Za-z]+-?['0-9A-Za-z]+\"\n",
        "print(len(regex_find_words(BOOK_TEXT, pattern)))"
      ],
      "execution_count": 18,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "70824\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "With a few quick changes, we can quickly see the power of using a regular expression to find different token patterns in the text. We now have 70824 tokens!\n",
        "\n",
        "**Note:** since the hyphen `-` is a single character we do not have to enclose that in brackets. We don't have to use `[-]?` but instead we can just use `-?` within the pattern.\n",
        "\n",
        "Don't worry, after a while reading the patterns becomes much easier. The hardest thing to understand is the `+-?` in the middle. Here's how you would read the pattern:\n",
        "\n",
        "\"1 or more (that's the `+`) characters that can be a single quote, letter, or number; FOLLOWED by a hyphen (`-`) that is optional (`?`) FOLLOWED by 1 or more (the very last +) characters that are either a single quote, a letter or a number.\"\n",
        "\n",
        "The remaining issue is that this pattern forces all words to be at least 2 characters long. We lose all the single character tokens (e.g. a, 4, 3, o) but we gain some context in words such as, \"whale-fishing\", or \"self-educated\". For these books and assignments we will give priority to the composed tokens over single-character tokens, such as 'a', since they bare more interesting information to us. However when you work on your own projects, you may need those single-character tokens,"
      ],
      "metadata": {
        "id": "gC397DrolXmk"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "#**A Few Regular Expression Mechanics**\n",
        "We now have seen enough to realize there's probably a lot of mechanics to learn about using regular expressions. You won't have to ever memorize them, but you should know what you can do. You can always look up the syntax later.\n",
        "\n",
        "##**Specific Sequences**\n",
        "If you wanted to find a specific string, you can just specify the exact order:\n",
        "```\n",
        "pattern = r\"self-control\"\n",
        "```\n",
        "This pattern would read \"find the word self followed by a dash and then followed by the word control\".\n",
        "\n",
        "Check how many of this are in the `BOOK_TEXT`, using the pattern with the `regex_find_words`\n",
        "\n"
      ],
      "metadata": {
        "id": "uJ45kih3hTYf"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Test the pattern"
      ],
      "metadata": {
        "id": "LP0ICwtehSpG"
      },
      "execution_count": 19,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Character Sets**\n",
        "The **square brackets** `[]` are used to hold multiple characters or character sets that can occur *in any order*.\n",
        "\n",
        "`[abc]` matches a or b or c `[abc]+` matches any combination of the letters: a, b, c\n",
        "```\n",
        "pattern = r\"col[ou]+r\"\n",
        "```\n",
        "This pattern would find words that starts with `col` followed by any combination of `o`s and `u`s followed by an `r`.\n",
        "\n",
        "This pattern would match both the american and the english spelling of col**o**r/col**ou**r. Do you see why?"
      ],
      "metadata": {
        "id": "xjxLbi8-hZdk"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Test the pattern for BOOK_TEXT to see what spelling do they use"
      ],
      "metadata": {
        "id": "UZtFz8uYhdvj"
      },
      "execution_count": 20,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "9lq09t9aPS4J"
      },
      "source": [
        "# **Regex Cheatsheet**"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Matching Specific Counts of Characters**\n",
        "We already have seen the `+` (1 or more of the previous character set). The following shows how to specify the number of match counts that can be used after a pattern:\n",
        "```\n",
        "?     0 or 1 time\n",
        "*     0 or more times\n",
        "+     1 or more times\n",
        "{m}   m times\n",
        "{m,}  at least m times\n",
        "{,n}  0 through n times (inclusive)\n",
        "{m,n} m through n times (inclusive)\n",
        "```\n",
        "The following pattern, specifies that the match must include two or more l's:\n",
        "\n",
        "```\n",
        "pattern = r\"P[eoh]+l{2,}\"\n",
        "```\n",
        "We'll see some more examples of these soon."
      ],
      "metadata": {
        "id": "B9bVuoojuKvk"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Try the count characters"
      ],
      "metadata": {
        "id": "rVNuZ8Z2kq_F"
      },
      "execution_count": 21,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Character Classes and Special Symbols**\n",
        "The following can be used to specify matching a character or a set of characters:\n",
        "```\n",
        ".  match any character except \\n\n",
        "\\. match the period\n",
        "\\? match the question mark\n",
        "\\s match whitespace \\s+ one or more white spaces\n",
        "\\S match non whitespace\n",
        "\\d match digits (same as [0-9])\n",
        "\\D non digits (same as [^0-9])\n",
        "\\w same as [a-zA-Z0-9_]+  (word character)\n",
        "\\W same as [^a-zA-Z0-9_]+ (non word character or non alphanumeric)\n",
        "\\' match a single quote\n",
        "\\\" match a double quote\n",
        "```\n",
        "###**Example**\n",
        "As an example, the pattern `\".o{2}.[ed]\"` will match any letter (the `.`) followed by 2 o's (`o{2}`) followed by any letter (`.`) and then followed either by an e or a d (`[ed]`).\n",
        "So this pattern would match: looke, hoose, cooke. Note that these are most likely partial word matches. But that's correct since we didn't specify any white space or word boundaries (to be discussed later)."
      ],
      "metadata": {
        "id": "7HhHgXYkkr91"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Try the example here"
      ],
      "metadata": {
        "id": "PLrGl_Zekwnw"
      },
      "execution_count": 22,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Special Characters**\n",
        "In a character set (the square brackets) any character in the brackets is a literal (meaning it doesn't represent something else). However, there are four characters that are exceptions to this:\n",
        "1. `^`: Anti-Match\n",
        "2. `-`: Range character\n",
        "3. `]`: Closure of the character set\n",
        "4. `\\`: Scape special characters\n",
        "\n",
        "For instance, if you wanted to match a caret `^` you would have to escape it (e.g. `[\\^abc]`) using the backslash `\\` .\n"
      ],
      "metadata": {
        "id": "xe16Yw2Nk0x5"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Try the special characters in a pattern"
      ],
      "metadata": {
        "id": "598zya85k3Jd"
      },
      "execution_count": 23,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**The Anti-Match ^**\n",
        "If you want to match anything BUT a specific character class, you add the caret `^` as the first item in square brackets:\n",
        "\n",
        "`[^abc]` matches anything BUT a or b or c. The caret 'negates' everything that follows.\n",
        "\n",
        "This shows why the `^` is considered a special character when used inside brackets."
      ],
      "metadata": {
        "id": "tzBzNRbFk6Ed"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Try the anti-match character in a pattern"
      ],
      "metadata": {
        "id": "hajIKjCnmJ7i"
      },
      "execution_count": 24,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Ignore case simplification**\n",
        "\n",
        "As we have seen, the regular expression pattern can get a bit long and we are always striving to keep the pattern as short and readable as possible. We can clean up the pattern by telling the compiler of the regular expression to ignore case:"
      ],
      "metadata": {
        "id": "jgEycEgFmBss"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "IIoxUZHRPS4L",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "1202229a-c9a9-4e96-e1d9-33fd4950e77d"
      },
      "source": [
        "def find_words_v1(text):\n",
        "  pattern = '[a-z0-9_]+'\n",
        "  regex   = re.compile(pattern, re.IGNORECASE)\n",
        "  return regex.findall(text)\n",
        "\n",
        "print(len(find_words_v1(BOOK_TEXT)))"
      ],
      "execution_count": 25,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "75364\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "\n",
        "Since we want to ignore the case (i.e. case insensitive) for the entire pattern we just pass the `re.IGNORECASE` flag to the compiler.\n",
        "\n",
        "This is such a popular pattern that Python provides a special character (`\\w`) that represents the pattern above (including being case insensitive). Either create a new code cell or add the code to a previous one:\n",
        "\n",
        "```\n",
        "def find_words_v2(text):\n",
        "  pattern = r'\\w+'\n",
        "  regex   = re.compile(pattern)\n",
        "  return regex.findall(text)\n",
        "  \n",
        "```\n",
        "However, notice that `\\w` also include the `_` character.\n",
        "\n",
        "**A shorter pattern for Frankenstein**\n",
        "\n",
        "We can still make the pattern for Frankenstein shorter, by using the `\\d` instead of `[0-9]`, and adding the flag to ignore the case like this:\n",
        "```\n",
        "def find_words_v3(text):\n",
        "  pattern = r\"['\\da-z]+-?['\\da-z]+\"\n",
        "  regex   = re.compile(pattern, re.IGNORECASE)\n",
        "  return regex.findall(text)\n",
        "  \n",
        "```"
      ],
      "metadata": {
        "id": "1kDnA_NKp29d"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# test the shorten pattern"
      ],
      "metadata": {
        "id": "qX-F_EDhqYuY"
      },
      "execution_count": 26,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Greedy Matching ***\n",
        "One thing (among many) to remember is that the regular expression engine will try to match the longest string possible. It's called greedy matching. You can change that behavior, but we will save that for another lesson. So if you have the pattern:"
      ],
      "metadata": {
        "id": "55hEL_UQqL_Y"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Yg1-4qgcPS4Q",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "72e889ab-2124-47c2-c2b5-bf96e59d6ae2"
      },
      "source": [
        "def find_words_v4(text):\n",
        "  pattern = r'ab.*'\n",
        "  reg_ex = re.compile(pattern, re.IGNORECASE)\n",
        "  return reg_ex.findall(text)\n",
        "\n",
        "text = \"Abra abracadabra\"\n",
        "print(find_words_v4(text))"
      ],
      "execution_count": 27,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "['Abra abracadabra']\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "This will match the entire string (and NOT 3 different 'ab' substrings). In general if you have `.*` in your regular expression, it will most likely match more than you want it too. In almost all cases, the greed will harm you."
      ],
      "metadata": {
        "id": "dK_-dkEfqtBM"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**More By Example**\n",
        "###**Finding Italicized**\n",
        "As a data scientist, it's important to be very familiar with the data being processed. In this case after reading some of the raw text we notice that for this book, italicized words or phrases are encoded by surrounding the word with an underscore. In Frankenstein, for example, at the beggining of the first letter the text:\n",
        "\n",
        "> _To Mrs. Saville, England._\n",
        "\n",
        "Get's encoded as follows:\n",
        "```\n",
        "_To Mrs. Saville, England._\n",
        "```\n",
        "Here's a quick example to find all italicized words: (those that begin and end with an underscore):"
      ],
      "metadata": {
        "id": "mw85NxM9wlDb"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import re\n",
        "def get_uniq_wordset(words):\n",
        "  return set([x.lower() for x in words])"
      ],
      "metadata": {
        "id": "AQwExUcaI4-r"
      },
      "execution_count": 28,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "6z9v3kCLPS4S",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "39a118fc-1961-49e7-b53f-7f718ea001fb"
      },
      "source": [
        "def find_words_v5(text):\n",
        "  pattern = r\"_[^_]+_\"\n",
        "  regex   = re.compile(pattern)\n",
        "  return regex.findall(text)\n",
        "\n",
        "uniq = get_uniq_wordset(find_words_v5(BOOK_TEXT))\n",
        "print(len(uniq), uniq)"
      ],
      "execution_count": 29,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "33 {'_honour_', '_schiavi ognor frementi,_', '_acme_', '_aiguilles_', '_shall_', '_campagne_', '_ennui_', '_maladie du pays_', '_i will be with you on\\nyour wedding-night._', '_keeping;_', '_ruins\\nof empires_', '_sorrows of werter_', '_good,\\ndearest, unhappy._', '_paradise lost_', '_son_', '_you_', '_good\\nspirit, wonderful_', '_sister_', '_in continuation._', '_to be with me on my wedding-night_', '_i will be with you on your\\nwedding-night!_', '_plutarch’s lives_', '_i shall be with\\nyou on your wedding-night_', '_felix, brother,_', '_dôme_', '_i_', '_to mrs. saville, england._', '_fire, milk, bread,_', '_father._', '_agatha,_', '_wives,_', '_wood._', '_he_'}\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "You should find 33 words that were emphasized in the book."
      ],
      "metadata": {
        "id": "zQlOzBxYrELy"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "###**Finding Digits**\n",
        "To find all the tokens with only digits in them, we just update the pattern:"
      ],
      "metadata": {
        "id": "NOC6xtRTxHp3"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "hpuCh9eqPS4T",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "081448b6-769a-4123-ba91-6715255bc28b"
      },
      "source": [
        "def find_words_v6(text):\n",
        "  pattern = r\"[0-9]+\"\n",
        "  regex   = re.compile(pattern)\n",
        "  return regex.findall(text)\n",
        "\n",
        "uniq = get_uniq_wordset(find_words_v6(BOOK_TEXT))\n",
        "print(len(uniq))"
      ],
      "execution_count": 30,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "28\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "We now can extract the 28 unique numeric tokens by printing them (left to the reader)."
      ],
      "metadata": {
        "id": "rwlwaLbpxE2s"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "###**Experimenting**\n",
        "When testing regular expressions, it's easier to work with a small sample of text to see if things are working or not. You can always extract a paragraph of text from your book and test (using set differences) between different patterns, what they match and what they don't.\n",
        "\n",
        "For example:\n",
        "```\n",
        "sentence = \"The girl was called _sister_ or _Agatha,_ and the youth _Felix, brother,_ or _son_. I cannot describe the delight I felt when I learned the ideas appropriated to each of these sounds and was able to pronounce them. I distinguished several other words without being able as yet to understand or apply them, such as _good, dearest, unhappy._\"\n",
        "print(find_words_v5(sentence))\n",
        "```"
      ],
      "metadata": {
        "id": "yPbCUvOPrOs5"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Try the example here"
      ],
      "metadata": {
        "id": "-ugTizKyw9KG"
      },
      "execution_count": 31,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Additional Normalization**\n",
        "You also can decide if you need to post normalize your tokens. It usually depends on the project's goals and objectives and the regular expression used. For example, the following could be done with the results from `findall()`:\n",
        "\n",
        "* removing whitespace before or after the token\n",
        "* case normalization\n",
        "* replacing the contractions with the fully spelled set of words (e.g. can't becomes cannot)\n",
        "* decide on common spelling (e.g. can not becomes cannot)\n",
        "* removing the plural (e.g songs become song)\n",
        "* fix spelling errors\n",
        "* stemming (a topic to be discussed in another lesson) which is similar to extracting the root of a word. We will leave all the tokens alone."
      ],
      "metadata": {
        "id": "p_9W231Hw8Nj"
      }
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "5cWCfGiGPS4T"
      },
      "source": [
        "#**Lesson Assignment**\n",
        "There is a lot to learn in this lesson. Be sure to **re-read** it and type&run all the examples.\n",
        "\n",
        "For all the questions in this lesson, you don't need to consult external documentation (you can of course, but everything required to solve these puzzles is given to you).\n",
        "\n",
        "**Notes:**\n",
        "\n",
        "* If you already know regular expressions and perhaps know a different solution, you still MUST ONLY USE what is taught in this lesson. Otherwise, you may not pass the tests.\n",
        "* Do NOT normalize the input or output. The tests are only looking at the results of the regular expression.\n",
        "* Use https://regex101.com for an easier way to develop/debug a working regular expression (or see the Coder's Log on using chrome's developer's tool)\n",
        "* Testing hints are given at the end\n",
        "* **Do NOT use the 'or' symbol** (e.g the pipe: `|`) -- it's something that will be covered in the next lesson. For any question that asks to find 'this or that', you need to use a standard regular expression shown in this lesson.\n",
        "\n",
        "The answer to each question is the result of using re.compile. All the questions will be using the text from Frankentein (BOOK_TEXT).\n",
        "\n",
        "The first question is done for you to see how to format your answers."
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Question 0: Total Sentences**\n",
        "**Write the regular expression to find all the sentences.**\n",
        "\n",
        "Assume that all sentences end with one of the following three punctuation marks: `?` `!` `.`\n",
        "\n",
        "**Answer:**"
      ],
      "metadata": {
        "id": "FSxA_qJ5xsMx"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "C7vZ6CdwPS4U"
      },
      "source": [
        "def q0():\n",
        "  pattern = r'[^?.!]+[?.!]+'\n",
        "  return re.compile(pattern, re.IGNORECASE)"
      ],
      "execution_count": 32,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "Which you read as \"1 or more of any character that is NOT a terminator followed by at least one terminator. A terminator is one of (`?` `.` `!`)\".\n",
        "\n",
        "#####**Testing**\n",
        "Once you have the question return the result of `re.compile`, you can test it as follows:"
      ],
      "metadata": {
        "id": "x0ioFCoi84vx"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "j3T1s1zyPS4V",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "2ea27c05-fa2d-4552-bbd3-88522bdcd482"
      },
      "source": [
        "# Extraction of a 'clean' part of the book (only actual book content)\n",
        "end_idx = BOOK_TEXT.find(\"*** END OF THE PROJECT\")\n",
        "clean = read_frankenstein()[book_idx:end_idx]\n",
        "\n",
        "reg_ex = q0()\n",
        "result = reg_ex.findall(clean)\n",
        "size = len(result)\n",
        "print(size, result[size-3:])  # show the last 3"
      ],
      "execution_count": 33,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "3378 ['\\nFarewell.', '”\\n\\nHe sprang from the cabin-window as he said this, upon the ice raft\\nwhich lay close to the vessel.', ' He was soon borne away by the waves and\\nlost in darkness and distance.']\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "You should get 3378 sentences (based on our definition) from the `clean_frankenstein.tx.` version of the book. **Take into account that all hints refer to the results using this version.**\n",
        "\n",
        "If you wanted to capture the ending `\"` in sentences, you would add the quote:\n",
        "```\n",
        "pattern = r'[^?.!]+[?.!\"]'\n",
        "```\n",
        "\n",
        "If you wanted to include any extra punctuation that ends some sentences (sentences that end like with `!!!!`) you could add the `+` at the end:\n",
        "```\n",
        "pattern = r'[^?.!]+[?.!\"]+'\n",
        "```\n",
        "Note that the following sentence would be considered 2 sentences:\n",
        "```\n",
        "Mr. Kean played Richmond.\n",
        "```\n",
        "\n",
        "So that 3378 is an approximation. We can do better, but the regular expression required would become very complex and involve more mechanics that we need to learn.\n",
        "\n",
        "The best way to solve this is to FIRST define some sample text:\n"
      ],
      "metadata": {
        "id": "C9lYaVqC_xbg"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "kX59epv5PS4W",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "e04ecb3f-a7df-418a-a07a-8d562f76be73"
      },
      "source": [
        "def test_q0():\n",
        "   sample = \"And now, dear Margaret, do I not deserve to accomplish some great purpose? My life might have been passed in ease and luxury, but I preferred glory to every enticement that wealth placed in my path. Oh, that some encouraging voice would answer in the affirmative!\"\n",
        "   reg_ex = q0()\n",
        "   result = reg_ex.findall(sample)\n",
        "   print(len(result))\n",
        "test_q0()"
      ],
      "execution_count": 34,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "3\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "\n",
        "You get 3 for an answer. You can verify that by hand. Once you have it working on sample text, then try it on `clean_frankenstein`.\n",
        "\n",
        "* all of your answers should be in the same format as `q0`.\n",
        "* return a compiled regular expression (with any flag if necessary).\n",
        "* the ONLY flag (if we use one) will be `re.IGNORECASE`. There are other flags, but those will be used in subsequent lessons.\n",
        "* Compare the hint with the counts for `clean_frankenstein`\n",
        "\n",
        "Before asking for help. Be sure to test each part of your answer. Test it with a few words, a short sentence, a long paragraph. Now that you know how to slice and dice an array, it's easy to extract sections of text."
      ],
      "metadata": {
        "id": "bWB9yuncB_2z"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Question 1: Double Digits**\n",
        "*Define the regular expression to answer*\n",
        "\n",
        "How many times does a double digit number appear?\n",
        "\n",
        "*hint: 37*"
      ],
      "metadata": {
        "id": "APMvaWBoy3jH"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "fYahrifGPS4X"
      },
      "source": [
        "def q1():\n",
        "    pattern = r'\\d{2}'\n",
        "    return re.compile(pattern)"
      ],
      "execution_count": 35,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Question 2: only numbers please**\n",
        "*Define the regular expression to answer*\n",
        "\n",
        "How many tokens consist of only numbers?\n",
        "\n",
        "*hint: 57*"
      ],
      "metadata": {
        "id": "fr50t_dmCvxU"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "x0EgDHuWPS4Y"
      },
      "source": [
        "def q2():\n",
        "    pattern = r'\\d+'\n",
        "    return re.compile(pattern)"
      ],
      "execution_count": 36,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Question 3: question mark?**\n",
        "*Define the regular expression to answer*\n",
        "\n",
        "How many question marks are in the text?\n",
        "\n",
        "**Note:** the `?` has special meaning, you will need to escape it.\n",
        "\n",
        "*hint: 220*"
      ],
      "metadata": {
        "id": "CKRnAXB8C2QL"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "t8XAnStAPS4a"
      },
      "source": [
        "def q3():\n",
        "    pattern = r'\\?'\n",
        "    return re.compile(pattern)"
      ],
      "execution_count": 37,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Question 4: three-parters**\n",
        "*Define the regular expression to answer*\n",
        "\n",
        "How many times are there two instances of a single dash within a word?\n",
        "\n",
        "E.g., \"brother-in-law\"\n",
        "\n",
        "**Note** A word consists of only letters.\n",
        "\n",
        "*hint: 2*"
      ],
      "metadata": {
        "id": "rGIRxtdTC8w0"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "6ztVIpHwPS4b"
      },
      "source": [
        "def q4():\n",
        "    pattern = r'[a-zA-Z]+-[a-zA-Z]+-[a-zA-Z]+'\n",
        "    return re.compile(pattern)"
      ],
      "execution_count": 38,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Question 5: Sometimes all we need is some time**\n",
        "*Define the regular expression to find*\n",
        "\n",
        "**sometimes** or **some time** ignoring the case.\n",
        "\n",
        "Note that \"some time\" can be also separated by a change of line\n",
        "\n",
        "\n",
        "*hint: 72*"
      ],
      "metadata": {
        "id": "0mM6s1DtDEZ0"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "YBtfmZPFPS4e"
      },
      "source": [
        "def q5():\n",
        "    pattern = r'some\\s*times?'\n",
        "    return re.compile(pattern, re.IGNORECASE)"
      ],
      "execution_count": 39,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Question 6: Double Quoting**\n",
        "*Define the regular expression to answer*\n",
        "\n",
        "How many times there is a double quotation mark followed by a single quotation mark (or vice-versa) in the text?\n",
        "\n",
        "**Note:** Remember that in Frankenstein the quotation characters used are either this `‘’` or this `“”`.\n",
        "\n",
        "\n",
        "*hint: 21*\n",
        "\n"
      ],
      "metadata": {
        "id": "xh9bzUzTDRKB"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "c8ZhazDdPS4f"
      },
      "source": [
        "def q6():\n",
        "    pattern = '[\\u201c\\u201d\\u2018\\u2019][\\u201c\\u201d\\u2018\\u2019]'\n",
        "    return re.compile(pattern)"
      ],
      "execution_count": 45,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Question 7: the Mr. and Mrs.**\n",
        "*Define the regular expression to find*\n",
        "\n",
        "any of the following (includes the period):` Dr.`, `Mr.`, or `Mrs.`\n",
        "\n",
        "**Note:** You need to match that specific letter case as well\n",
        "\n",
        "*hint: 17*"
      ],
      "metadata": {
        "id": "0xNhwvDNDaD5"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "_ItvohyTPS4h"
      },
      "source": [
        "def q7():\n",
        "    pattern = r'[DM]rs?\\.'\n",
        "    return re.compile(pattern)"
      ],
      "execution_count": 41,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Question 8: More than a monster**\n",
        "*Define the regular expression to find*\n",
        "\n",
        "any word that contains \"monst\"\n",
        "\n",
        "**Note:**\n",
        "* this is a regular expression where you could use the greedy `*`\n",
        "* a word consists of only letters\n",
        "* capitalization is not relevant\n",
        "\n",
        "*hint: 39*"
      ],
      "metadata": {
        "id": "5ZmDeoQjDg4R"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "xacJrvACPS4j"
      },
      "source": [
        "def q8():\n",
        "    pattern = r'[a-z]*monst[a-z]*'\n",
        "    return re.compile(pattern, re.IGNORECASE)"
      ],
      "execution_count": 42,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "##**Question 9: Some pronouns**\n",
        "*Define the regular expression to find*\n",
        "\n",
        "either **her, hers, him** or **his**\n",
        "\n",
        "**Note:**\n",
        "* You CANNOT use the keyword 'or' or the | symbol\n",
        "* capitalization is not relevant\n",
        "* each must be surrounded by whitespace so the 'him' in 'himself' would not be found.\n",
        "\n",
        "*hint: 1011*\n",
        "\n",
        "*if you are stuck or unsure how to proceed, recall what the [ ] can do to help with matching*"
      ],
      "metadata": {
        "id": "6CvzPUYHDpyR"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "oiCaQD3OPS4k"
      },
      "source": [
        "def q9():\n",
        "    pattern = r'\\sh[ei][rms]s?\\s'\n",
        "    return re.compile(pattern, re.IGNORECASE)"
      ],
      "execution_count": 43,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "#**Question 10: How many chapters?**\n",
        "*Define the regular expression to find*\n",
        "\n",
        "The chapter (not letters) markers in Frankenstein.\n",
        "\n",
        "**Note:**\n",
        "* a chapter is defined as a title such as \"Chapter 1\"\n",
        "\n",
        "*hint: 24*"
      ],
      "metadata": {
        "id": "e2k5yfxyDyvp"
      }
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "tt8dlJUBPS4l"
      },
      "source": [
        "def q10():\n",
        "    pattern = r'Chapter \\d+'\n",
        "    return re.compile(pattern)"
      ],
      "execution_count": 44,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "vMt_MbqBPS4p"
      },
      "source": [
        "##**Submission**\n",
        "\n",
        "After implementing all the functions and testing them please download the notebook as \"info407_regex_part_1.py\" and submit it to Gradescope under the \"RegEx Part 1\" assignment tab.\n",
        "\n",
        "**NOTES**\n",
        "\n",
        "* Be sure to use the function names and parameter names as given.\n",
        "* DO NOT use your own function or parameter names.\n",
        "* Your file MUST be named \"info407_regex_part_1.py\".\n",
        "* Comment out any lines of code and/or function calls to those functions that produce errors.\n",
        "* Grading cannot be performed if any of these are violated."
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "\n",
        "###**Readings**\n",
        "Python Docs\n",
        "* https://docs.python.org/3.6/library/re.html\n",
        "\n",
        "Testing Frameworks\n",
        "\n",
        "* https://www.regextester.com/97589\n",
        "* https://pythex.org\n",
        "* https://www.regular-expressions.info\n",
        "\n",
        "CheatSheets\n",
        "\n",
        "* https://cdn.activestate.com/wp-content/uploads/2020/03/Python-RegEx-Cheatsheet.pdf\n",
        "* https://www.tutorialspoint.com/python/python_reg_expressions.htm"
      ],
      "metadata": {
        "id": "x3N4NewT9oLi"
      }
    }
  ]
}