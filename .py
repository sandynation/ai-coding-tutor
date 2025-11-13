"""
AI Coding Tutor System
A comprehensive learning platform that provides personalized coding guidance
"""

import json
import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ProgrammingLanguage(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "c++"


class ProblemCategory(Enum):
    ALGORITHMS = "algorithms"
    DATA_STRUCTURES = "data_structures"
    WEB_DEVELOPMENT = "web_development"
    MACHINE_LEARNING = "machine_learning"


class CodeAnalysis:
    """Analyzes student code for quality and correctness"""
    
    def __init__(self):
        self.common_issues = {
            'python': {
                'inefficient_loops': "Consider using list comprehensions or built-in functions",
                'missing_docstrings': "Add docstrings to explain your functions",
                'poor_naming': "Use descriptive variable and function names",
                'no_error_handling': "Add try-except blocks for robust code",
                'hardcoded_values': "Use constants or configuration variables"
            }
        }
    
    def analyze_code_quality(self, code: str, language: ProgrammingLanguage) -> Dict:
        """Comprehensive code analysis with specific feedback"""
        analysis = {
            'score': 0,
            'suggestions': [],
            'warnings': [],
            'best_practices': []
        }
        
        # Basic code quality checks
        lines = code.split('\n')
        analysis['line_count'] = len(lines)
        
        # Check for common issues
        if language == ProgrammingLanguage.PYTHON:
            self._analyze_python_code(code, analysis)
        
        # Calculate overall score
        analysis['score'] = self._calculate_code_score(analysis)
        
        return analysis
    
    def _analyze_python_code(self, code: str, analysis: Dict) -> None:
        """Python-specific code analysis"""
        checks = [
            (lambda c: 'def ' in c and '"""' not in c and "'''" not in c, 
             self.common_issues['python']['missing_docstrings']),
            (lambda c: 'for ' in c and 'range(len(' in c, 
             self.common_issues['python']['inefficient_loops']),
            (lambda c: any(word in c for word in ['temp', 'var', 'data', 'value']),
             self.common_issues['python']['poor_naming']),
            (lambda c: 'input()' in c and 'try:' not in c,
             self.common_issues['python']['no_error_handling']),
            (lambda c: any(str(num) in c for num in [10, 100, 1000, 5]),
             self.common_issues['python']['hardcoded_values'])
        ]
        
        for check, message in checks:
            if check(code):
                analysis['suggestions'].append(message)


class CodingProblem:
    """Represents a coding problem with multiple difficulty levels"""
    
    def __init__(self, problem_id: str, title: str, description: str, 
                 category: ProblemCategory, language: ProgrammingLanguage,
                 difficulty: DifficultyLevel, test_cases: List[Tuple]):
        self.problem_id = problem_id
        self.title = title
        self.description = description
        self.category = category
        self.language = language
        self.difficulty = difficulty
        self.test_cases = test_cases
        self.hints = []
        self.solution_approach = ""
    
    def add_hint(self, hint: str, level: int = 1) -> None:
        """Add hierarchical hints - more specific hints have higher levels"""
        self.hints.append({'level': level, 'hint': hint})
    
    def get_hint(self, current_level: int) -> Optional[str]:
        """Get appropriate hint based on student's current struggle level"""
        available_hints = [h for h in self.hints if h['level'] <= current_level]
        return random.choice(available_hints)['hint'] if available_hints else None


class StudentProgress:
    """Tracks and manages student learning progress"""
    
    def __init__(self, student_id: str):
        self.student_id = student_id
        self.completed_problems = set()
        self.current_streak = 0
        self.longest_streak = 0
        self.skill_levels = {
            category: DifficultyLevel.BEGINNER 
            for category in ProblemCategory
        }
        self.performance_metrics = {}
    
    def update_progress(self, problem: CodingProblem, success: bool, 
                       code_quality_score: float) -> None:
        """Update student progress based on problem attempt"""
        if success:
            self.completed_problems.add(problem.problem_id)
            self.current_streak += 1
            self.longest_streak = max(self.longest_streak, self.current_streak)
            
            # Update skill level based on performance
            if code_quality_score > 80 and problem.difficulty == self.skill_levels[problem.category]:
                self._promote_skill_level(problem.category)
        else:
            self.current_streak = 0
    
    def _promote_skill_level(self, category: ProblemCategory) -> None:
        """Promote student to next difficulty level in a category"""
        current = self.skill_levels[category]
        if current == DifficultyLevel.BEGINNER:
            self.skill_levels[category] = DifficultyLevel.INTERMEDIATE
        elif current == DifficultyLevel.INTERMEDIATE:
            self.skill_levels[category] = DifficultyLevel.ADVANCED


class AICodingTutor:
    """Main AI Coding Tutor class that orchestrates the learning experience"""
    
    def __init__(self):
        self.code_analyzer = CodeAnalysis()
        self.problems = self._initialize_problems()
        self.students = {}
        self.session_history = []
    
    def _initialize_problems(self) -> Dict[str, CodingProblem]:
        """Initialize a set of sample coding problems"""
        problems = {}
        
        # Problem 1: Fibonacci Sequence
        fib_problem = CodingProblem(
            problem_id="fib_001",
            title="Fibonacci Sequence Generator",
            description="Write a function that returns the nth Fibonacci number.",
            category=ProblemCategory.ALGORITHMS,
            language=ProgrammingLanguage.PYTHON,
            difficulty=DifficultyLevel.BEGINNER,
            test_cases=[
                ((0,), 0),
                ((1,), 1),
                ((5,), 5),
                ((10,), 55)
            ]
        )
        fib_problem.add_hint("The Fibonacci sequence starts with 0 and 1")
        fib_problem.add_hint("Each subsequent number is the sum of the previous two")
        fib_problem.add_hint("Consider using recursion or iteration")
        problems[fib_problem.problem_id] = fib_problem
        
        # Problem 2: Palindrome Checker
        palindrome_problem = CodingProblem(
            problem_id="pal_001",
            title="Palindrome Checker",
            description="Write a function that checks if a string is a palindrome.",
            category=ProblemCategory.ALGORITHMS,
            language=ProgrammingLanguage.PYTHON,
            difficulty=DifficultyLevel.BEGINNER,
            test_cases=[
                (("racecar",), True),
                (("hello",), False),
                (("A man a plan a canal Panama",), True),
                (("",), True)
            ]
        )
        palindrome_problem.add_hint("A palindrome reads the same forwards and backwards")
        palindrome_problem.add_hint("Consider removing spaces and converting to lowercase")
        palindrome_problem.add_hint("You can reverse the string and compare")
        problems[palindrome_problem.problem_id] = palindrome_problem
        
        return problems
    
    def register_student(self, student_id: str) -> StudentProgress:
        """Register a new student"""
        if student_id not in self.students:
            self.students[student_id] = StudentProgress(student_id)
        return self.students[student_id]
    
    def get_recommended_problem(self, student_id: str, 
                               category: Optional[ProblemCategory] = None) -> CodingProblem:
        """Get a problem recommendation based on student's skill level"""
        student = self.students[student_id]
        
        if category is None:
            # Recommend category where student needs most practice
            category = random.choice(list(ProblemCategory))
        
        target_difficulty = student.skill_levels[category]
        
        # Find problems matching category and difficulty
        suitable_problems = [
            p for p in self.problems.values() 
            if p.category == category and p.difficulty == target_difficulty
            and p.problem_id not in student.completed_problems
        ]
        
        if not suitable_problems:
            # Fallback to any problem at appropriate difficulty
            suitable_problems = [
                p for p in self.problems.values() 
                if p.difficulty == target_difficulty
                and p.problem_id not in student.completed_problems
            ]
        
        return random.choice(suitable_problems) if suitable_problems else list(self.problems.values())[0]
    
    def submit_solution(self, student_id: str, problem_id: str, 
                       code: str) -> Dict:
        """Process student code submission and provide feedback"""
        student = self.students[student_id]
        problem = self.problems[problem_id]
        
        # Analyze code quality
        analysis = self.code_analyzer.analyze_code_quality(code, problem.language)
        
        # Test the code (simplified - in reality, you'd execute in a sandbox)
        test_results = self._run_tests(code, problem.test_cases)
        
        # Update student progress
        success_rate = sum(1 for result in test_results if result['passed']) / len(test_results)
        student.update_progress(problem, success_rate > 0.8, analysis['score'])
        
        # Log session
        self._log_session(student_id, problem_id, success_rate, analysis['score'])
        
        return {
            'test_results': test_results,
            'code_analysis': analysis,
            'success_rate': success_rate,
            'next_recommendation': self.get_recommended_problem(student_id, problem.category),
            'encouragement': self._generate_encouragement(success_rate, analysis['score'])
        }
    
    def _run_tests(self, code: str, test_cases: List[Tuple]) -> List[Dict]:
        """Simulate test execution (in practice, use secure code execution)"""
        results = []
        
        for i, (inputs, expected) in enumerate(test_cases):
            try:
                # Note: In production, use secure code execution environment
                # This is a simplified simulation
                result = {
                    'test_case': i + 1,
                    'inputs': inputs,
                    'expected': expected,
                    'passed': random.random() > 0.3,  # Simulated result
                    'actual': expected if random.random() > 0.3 else "different_result"
                }
            except Exception as e:
                result = {
                    'test_case': i + 1,
                    'inputs': inputs,
                    'expected': expected,
                    'passed': False,
                    'error': str(e)
                }
            results.append(result)
        
        return results
    
    def _generate_encouragement(self, success_rate: float, quality_score: float) -> str:
        """Generate encouraging feedback based on performance"""
        if success_rate > 0.9 and quality_score > 85:
            return "Excellent work! Your solution is both correct and well-written!"
        elif success_rate > 0.7:
            return "Good job! You're on the right track. Keep practicing!"
        else:
            return "Don't give up! Every programmer faces challenges. Review the hints and try again!"
    
    def _log_session(self, student_id: str, problem_id: str, 
                    success_rate: float, quality_score: float) -> None:
        """Log learning session for analytics"""
        session = {
            'student_id': student_id,
            'problem_id': problem_id,
            'timestamp': datetime.now().isoformat(),
            'success_rate': success_rate,
            'quality_score': quality_score
        }
        self.session_history.append(session)


# Example usage and demonstration
def demonstrate_tutor():
    """Demonstrate the AI Coding Tutor in action"""
    tutor = AICodingTutor()
    
    # Register a student
    student = tutor.register_student("student_123")
    
    print("🤖 Welcome to AI Coding Tutor!")
    print("=" * 50)
    
    # Get recommended problem
    problem = tutor.get_recommended_problem("student_123")
    print(f"Recommended Problem: {problem.title}")
    print(f"Category: {problem.category.value}")
    print(f"Difficulty: {problem.difficulty.value}")
    print(f"\nDescription: {problem.description}")
    
    # Simulate student submitting a solution
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
"""
    
    print(f"\n📝 Student Code Submission:")
    print(sample_code)
    
    # Submit solution and get feedback
    results = tutor.submit_solution("student_123", problem.problem_id, sample_code)
    
    print(f"📊 Results:")
    print(f"Success Rate: {results['success_rate']:.1%}")
    print(f"Code Quality Score: {results['code_analysis']['score']}/100")
    
    print(f"\n💡 Suggestions:")
    for suggestion in results['code_analysis']['suggestions'][:3]:
        print(f"  - {suggestion}")
    
    print(f"\n🎯 {results['encouragement']}")
    
    # Show student progress
    print(f"\n📈 Student Progress:")
    print(f"Completed Problems: {len(student.completed_problems)}")
    print(f"Current Streak: {student.current_streak} days")
    print(f"Skill Levels:")
    for category, level in student.skill_levels.items():
        print(f"  {category.value}: {level.value}")


if __name__ == "__main__":
    demonstrate_tutor()
