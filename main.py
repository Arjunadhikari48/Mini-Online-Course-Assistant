
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Mini Online Course Assistant")

@app.get("/")
def home():
    return{"message":"mini online  course assistant "}

class QuestionRequest(BaseModel):
    question: str

COURSES = [
    {
        "id": 1,
        "title": "Python Programming",
        "fee": 5000,
        "instructor": "Somenath Singha",
        "details": {
            "level": "Beginner",
            "duration": "3 months",
            "language": "English",
            "tools": ["Python", "PostgreSQL", "FastAPI"],
        },
    },
    {
        "id": 2,
        "title": "Java Programming",
        "fee": 6000,
        "instructor": "Arpita Roy",
        "details": {
            "level": "Intermediate",
            "duration": "4 months",
            "language": "English",
            "tools": ["Java", "MySQL", "DSA"],
        },
    },
    {
        "id": 3,
        "title": "Data Science",
        "fee": 8000,
        "instructor": "Ipshita Saha",
        "details": {
            "level": "Advanced",
            "duration": "6 months",
            "language": "English",
            "tools": ["Python", "Pandas", "NumPy"],
        },
    },
]
@app.get("/courses")
async def get_courses():
    """Return all courses"""
    return COURSES

@app.get("/courses/{course_id}")
async def get_course(course_id: int):
    """Return a single course by ID"""
    for course in COURSES:
        if course["id"] == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Handle natural language questions about courses"""
    question = request.question.strip()
    
    # Input validation
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Find best matching course
    best_course = find_best_course(question)
    
    # Build response
    return build_response(question, best_course)
def find_best_course(question):
    """
    Find the best matching course based on the question.
    Returns the course with the highest score, or None if no matches.
    """
    # Clean the question
    cleaned_question = question.lower()
    # Remove punctuation
    for punct in ".?!":
        cleaned_question = cleaned_question.replace(punct, "")
    # Split into words
    question_words = cleaned_question.split()
    
    best_course = None
    best_score = 0
    
    for course in COURSES:
        score = 0
        # Build searchable text from course fields
        searchable_text = (
            course["title"].lower() + " " +
            str(course["fee"]).lower() + " " +
            course["instructor"].lower() + " " +
            course["details"]["level"].lower() + " " +
            course["details"]["duration"].lower() + " " +
            course["details"]["language"].lower() + " " +
            " ".join([tool.lower() for tool in course["details"]["tools"]])
        )
        
        # Count matching words
        for word in question_words:
            if word in searchable_text:
                score += 1
        
        # Update best course if this one has a higher score
        if score > best_score:
            best_score = score
            best_course = course
    
    # Return the best course if it has at least one match
    if best_score > 0:
        return best_course, best_score
    return None, 0
def build_answer(course):
    """Build a grounded answer using only course information"""
    if course is None:
        return "Information not available in the supplied course data."
    
    tools_str = ", ".join(course["details"]["tools"])
    return (f"{course['title']} is a {course['details']['level']} course "
            f"taught by {course['instructor']}. Its duration is "
            f"{course['details']['duration']}, its fee is {course['fee']}, "
            f"and its tools include {tools_str}.")

def build_prompt(question, course):
    """Build a prompt for the RAG system"""
    if course is None:
        return None
    
    prompt = f"""ROLE: You are an online course assistant.
    
INSTRUCTION: Use only the supplied course information. Do not guess or invent information.

CONTEXT: 
Title: {course['title']}
Fee: {course['fee']}
Instructor: {course['instructor']}
Level: {course['details']['level']}
Duration: {course['details']['duration']}
Language: {course['details']['language']}
Tools: {', '.join(course['details']['tools'])}

QUESTION: {question}

Please provide an answer based solely on the information above."""
    
    return prompt

def build_response(question, best_course):
    """Build the complete API response"""
    if best_course is None:
        return {
            "question": question,
            "retrieved_course": None,
            "matched_keywords": [],
            "match_score": 0,
            "answer": "Information not available in the supplied course data.",
            "source": None,
            "prompt_preview": None
        }
    
    # Extract matched keywords from the question
    cleaned_question = question.lower()
    for punct in ".?!":
        cleaned_question = cleaned_question.replace(punct, "")
    question_words = cleaned_question.split()
    
    matched_keywords = []
    searchable_text = (
        best_course["title"].lower() + " " +
        str(best_course["fee"]).lower() + " " +
        best_course["instructor"].lower() + " " +
        best_course["details"]["level"].lower() + " " +
        best_course["details"]["duration"].lower() + " " +
        best_course["details"]["language"].lower() + " " +
        " ".join([tool.lower() for tool in best_course["details"]["tools"]])
    )
    
    for word in question_words:
        if word in searchable_text:
            matched_keywords.append(word)
    
    return {
        "question": question,
        "retrieved_course": best_course["title"],
        "matched_keywords": matched_keywords,
        "match_score": len(matched_keywords),
        "answer": build_answer(best_course),
        "source": best_course["title"],
        "prompt_preview": build_prompt(question, best_course)
    }

# Note: Make sure to update the ask_question function to use build_response
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    question = request.question.strip()
    
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    best_course, score = find_best_course(question)
    return build_response(question, best_course)
    
    
