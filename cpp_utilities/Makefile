CXX := g++
CXXFLAGS := -std=c++11 -Wall -I.

PARSER_SRCS := MarkdownToHTML.cpp html-element/HTMLElement.cpp sample-parser/Main.cpp
PARSER_OBJS := $(PARSER_SRCS:.cpp=.o)
PROGRAM_NAME := markdown-parser

all: parser

bin:
	mkdir -p bin

parser: bin $(PARSER_OBJS)
	$(CXX) $(CXXFLAGS) -o bin/$(PROGRAM_NAME) $(PARSER_OBJS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(PARSER_OBJS)

fclean: clean
	rm -rf bin/$(PROGRAM_NAME)

re: fclean all

.PHONY: all clean tests parser
