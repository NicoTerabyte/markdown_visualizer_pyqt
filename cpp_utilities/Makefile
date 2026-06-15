CXX := g++
CXXFLAGS := -std=c++17 -Wall -I.

PARSER_SRCS := MarkdownToHTML.cpp html-element/HTMLElement.cpp sample-parser/Main.cpp
PARSER_OBJS := $(PARSER_SRCS:.cpp=.o)

all: parser

bin:
	mkdir -p bin

parser: bin $(PARSER_OBJS)
	$(CXX) $(CXXFLAGS) -o bin/markdown-parser $(PARSER_OBJS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(PARSER_OBJS)

fclean: clean
	rm -rf bin

re: fclean all

.PHONY: all clean tests parser
