#include <string>
#include <list>
#include <map>
#include <iostream>
#include <memory>
#include <utility>

using namespace std;



class Element
{
protected:
	Element* parent = nullptr;
public:
	Element(){}
	virtual void generate(ostream& stream) const = 0;
	void setParent(Element* _parent) { parent = _parent; }
};

class HTMLElement : public Element
{
	string tag;
	list< shared_ptr<Element> > contents;
	list<pair<string,string>> attributes;

	bool single = false; // single tag ex: <br>
	void generateContents(ostream& stream) const;
	void generateAttributes(ostream& stream) const;
public:
	HTMLElement(string _tag);
	HTMLElement* setAttribute(const char* attr, const char* val);
	HTMLElement* setSingle(bool _single);
	HTMLElement* getParent() const { return dynamic_cast<HTMLElement*>(parent); }
	template<class T> T* appendChild(shared_ptr<T> child);
	void generate(ostream& stream) const;
};

class TextElement: public Element
{
	string textContent;
public:
	TextElement(string _textContent) : textContent(_textContent){}
	HTMLElement* getParent() const { return dynamic_cast<HTMLElement*>(parent); }
	void generate(ostream& stream) const
	{
		stream << textContent;
	}
};

//the template was declared in the cpp file causing a problem with the includes from the other files
template<class T>
T* HTMLElement::appendChild(shared_ptr<T> child)
{
	contents.push_back(child);

	shared_ptr<T> justAdded = dynamic_pointer_cast<T>(contents.back());

	justAdded->setParent(this);

	return justAdded.get();
}

shared_ptr<HTMLElement> make_HTMLElement(const char* tag);
shared_ptr<TextElement> make_TextElement(const char* text);
ostream& operator<<(ostream& stream, const Element& elem);

#pragma once
