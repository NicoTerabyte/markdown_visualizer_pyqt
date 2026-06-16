#include <iostream>
#include "MarkdownToHTML.h"

//Il booleano semplicemente mette in ordine head e body nella pagina html
MarkdownToHTML::MarkdownToHTML(bool generateFullPage)
{
	this->rootNode = make_shared<HTMLElement>((generateFullPage) ? "html" : "blank");
	cout<<"with generate page at "<<generateFullPage<<" we get "<< this->rootNode->get_tag()<<endl;
	if(generateFullPage)
	{
		this->rootNode->appendChild(make_HTMLElement("head"));
		this->insertionPoint = rootNode->appendChild(make_HTMLElement("body"));
	}
	else
	{
		cout<<"starting blank"<<endl;
		this->insertionPoint = this->rootNode.get();
	}
};

void MarkdownToHTML::processLine(string& input)
{
	processEscapeCharacters(input);

	sv_match matches;

	LineType currentLineType = determineLineType(input, matches);

	if(lineState == inCodeBlock && currentLineType != CodeBlock)
		currentLineType = Other;

	switch(currentLineType)
	{
	case Heading:
		processHeadingLine(matches);
		break;
	case UnorderedListItem:
		processUnorderedListItemLine(matches);
		break;
	case OrderedListItem:
		processOrderedListItemLine(matches);
		break;
	case CodeBlock:
		processCodeBlockLine(matches);
		break;
	case Table:
		processTableLine(matches);
		break;
	case Empty:
		processEmptyLine();
		break;
	case Other:
		processOtherLine(input);
	}
}

void MarkdownToHTML::processEscapeCharacters(string& input) const
{
	// Just '<' and '>' characters for now, no support for raw HTML tags
	input = regex_replace(input, regex("<"), "&lt;");
	input = regex_replace(input, regex(">"), "&gt;");
}

LineType MarkdownToHTML::determineLineType(const string& input, sv_match& matches)
{
	static const pair<const regex&, LineType> LineRegexAndTypes [] {
		{headingRegex, Heading},
		{unorderedListItemRegex, UnorderedListItem},
		{orderedListItemRegex, OrderedListItem},
		{codeRegex, CodeBlock},
		{tableRegex, Table},
		{emptyRegex, Empty},
	};

	for(const auto& lineRegexAndType : LineRegexAndTypes)
	{
		if(regex_match(input.begin(), input.end(), matches, lineRegexAndType.first))
			return lineRegexAndType.second;
	}

	return Other;
}

void MarkdownToHTML::processHeadingLine(const sv_match& matches)
{
	if(lineState != inNothing)
		throw exception();
	// number of #### claro
	int hSize = matches[1].length();
	string tag = "h" + to_string(hSize);

	auto heading = make_HTMLElement(tag.c_str());
	heading->appendChild(make_TextElement(matches[2].str().c_str()));

	insertionPoint->appendChild(heading);
}

void MarkdownToHTML::processUnorderedListItemLine(const sv_match& matches)
{
	if(lineState == inNothing)
	{
		auto ul = make_HTMLElement("ul");
		insertionPoint = insertionPoint->appendChild(ul);
		lineState = inUnorderedList;
	}

	auto li = make_HTMLElement("li");
	processSubExpressions(matches[1].str(), li);
	insertionPoint->appendChild(li);
}

void MarkdownToHTML::processOrderedListItemLine(const sv_match& matches)
{
	if(lineState == inNothing)
	{
		auto ol = make_HTMLElement("ol");
		insertionPoint = insertionPoint->appendChild(ol);
		lineState = inOrderedList;
	}

	auto li = make_HTMLElement("li");
	processSubExpressions(matches[2].str(), li);
	insertionPoint->appendChild(li);
}

void MarkdownToHTML::processCodeBlockLine(const sv_match& matches)
{
	if(lineState == inCodeBlock)
	{
		insertionPoint = insertionPoint->getParent();
		lineState = inNothing;
		return;
	}

	auto div = make_HTMLElement("div");
	div->setAttribute("class", "code");

	insertionPoint = insertionPoint->appendChild(div);
	lineState = inCodeBlock;
}

void MarkdownToHTML::processTableLine(const sv_match& matches)
{
	if(matches[0].str().find("---") != string::npos) // <th> underline
		return;

	// Decide whether td or th
	string tag_name;
	if(lineState != inTable)
	{
		insertionPoint = insertionPoint->appendChild(make_HTMLElement("table"));
		tag_name = "th";
		lineState = inTable;
	}
	else
	{
		tag_name = "td";
	}

	insertionPoint = insertionPoint->appendChild(make_HTMLElement("tr"));

	string cellValue;
	for(char c : matches[0].str())
	{
		if(c == '|')
		{
			auto cell = make_HTMLElement(tag_name.c_str());
			processSubExpressions(cellValue, cell);
			insertionPoint->appendChild(cell);

			cellValue.clear();
			continue;
		}
		cellValue += c;
	}

	auto cell = make_HTMLElement(tag_name.c_str());
	processSubExpressions(cellValue, cell);
	insertionPoint->appendChild(cell);
	insertionPoint = insertionPoint->getParent();
}

void MarkdownToHTML::processEmptyLine()
{
	if(lineState != inNothing)
	{
		lineState = inNothing;
		insertionPoint = insertionPoint->getParent();
	}
}

void MarkdownToHTML::processOtherLine(string& input)
{
	if(lineState == inUnorderedList || lineState == inOrderedList || lineState == inTable)
	{
		insertionPoint = insertionPoint->getParent();
		lineState = inNothing;
	}

	if(lineState == inNothing)
	{
		auto p = make_HTMLElement("p");
		processSubExpressions(input, p);

		insertionPoint = insertionPoint->appendChild(p);
		lineState = inParagraph;
	}

	if(lineState == inCodeBlock)
	{
		string htmlCompatible = regex_replace(input,regex("\\s"),"&nbsp;");
		htmlCompatible = regex_replace(htmlCompatible, regex("<"), "&lt;");
		htmlCompatible = regex_replace(htmlCompatible, regex(">"), "&gt;");


		insertionPoint->appendChild(make_TextElement(htmlCompatible.c_str()));

		auto br = make_HTMLElement("br");
		br->setSingle(true);
		insertionPoint->appendChild(br);
	}
}

void MarkdownToHTML::processSubExpressions(const string& input, shared_ptr<HTMLElement> parent)
{
	sv_match matches;
	ExpressionType currentExpression = determineExpressionType(input, matches);

	switch(currentExpression)
	{
		case Bold:
			processBoldExpression(input, matches, parent);
			break;
		case Italic:
			processItalicExpression(input, matches, parent);
			break;
		case Image:
			processImageExpression(input, matches, parent);
			break;
		case Link:
			processLinkExpression(input, matches, parent);
			break;
		case Text:
		default:
			processTextExpression(input, matches, parent);
	}
}

void MarkdownToHTML::processSubExpressionsBetween(string::const_iterator begin, string::const_iterator end, shared_ptr<HTMLElement> parent)
{
	processSubExpressions(string(begin, end), parent);
}

ExpressionType MarkdownToHTML::determineExpressionType(const string& input, sv_match& matches)
{
	static const pair<const regex&, ExpressionType> ExpressionRegexAndTypes [] {
		{boldRegex, Bold},
		{italicRegex, Italic},
		{imageRegex, Image},
		{linkRegex, Link},
	};

	for(const auto& expressionRegexAndType : ExpressionRegexAndTypes)
	{
		if(regex_search(input.begin(), input.end(), matches, expressionRegexAndType.first))
			return expressionRegexAndType.second;
	}

	return Text;
}

void MarkdownToHTML::processBoldExpression(const string& input, const sv_match& matches, shared_ptr<HTMLElement> parent)
{
	processSubExpressionsBetween(input.begin(), matches[0].first, parent);

	auto b = make_HTMLElement("b");
	processSubExpressionsBetween(matches[1].first, matches[1].second, b);
	parent->appendChild(b);

	processSubExpressionsBetween(matches[0].second, input.end(), parent);
}

void MarkdownToHTML::processItalicExpression(const string& input, const sv_match& matches, shared_ptr<HTMLElement> parent)
{
	processSubExpressionsBetween(input.begin(), matches[0].first, parent);

	auto i = make_HTMLElement("i");
	processSubExpressionsBetween(matches[1].first, matches[1].second, i);
	parent->appendChild(i);

	processSubExpressionsBetween(matches[0].second, input.end(), parent);
}

void MarkdownToHTML::processImageExpression(const string& input, const sv_match& matches, shared_ptr<HTMLElement> parent)
{
	processSubExpressionsBetween(input.begin(), matches[0].first, parent);

	auto img = make_HTMLElement("img");
	img
		->setAttribute("alt", matches[1].str().c_str())
		->setAttribute("src", matches[2].str().c_str());
	parent->appendChild(img);

	processSubExpressionsBetween(matches[0].second, input.end(), parent);
}

void MarkdownToHTML::processLinkExpression(const string& input, const sv_match& matches, shared_ptr<HTMLElement> parent)
{
	processSubExpressionsBetween(input.begin(), matches[0].first, parent);

	auto a = make_HTMLElement("a");
	a->setAttribute("href", matches[2].str().c_str());
	processSubExpressionsBetween(matches[1].first, matches[1].second, a);
	parent->appendChild(a);

	processSubExpressionsBetween(matches[0].second, input.end(), parent);
}

void MarkdownToHTML::processTextExpression(const string& input, const sv_match& matches, shared_ptr<HTMLElement> parent)
{
	parent->appendChild(make_TextElement(input.c_str()));
}

const HTMLElement& MarkdownToHTML::getcRootNode() const
{
	return *rootNode;
}

ostream& operator<<(ostream& stream, const MarkdownToHTML& parser)
{
	stream << parser.getcRootNode();
	return stream;
}
