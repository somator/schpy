import unittest

from sc_eval import Evaluator

evaluator = Evaluator()

class TestEval(unittest.TestCase):
    def test_int(self):
        self.assertEqual(486, evaluator.lex_parse_eval('486'))
    
    def test_addition(self):
        self.assertEqual(486, evaluator.lex_parse_eval('(+ 137 349)'))
    
    def test_subtraction(self):
        self.assertEqual(666, evaluator.lex_parse_eval('(- 1000 334)'))
    
    def test_multiplication(self):
        self.assertEqual(495, evaluator.lex_parse_eval('(* 5 99)'))

    def test_division(self):
        self.assertEqual(2, evaluator.lex_parse_eval('(/ 10 5)'))
    
    def test_float(self):
        self.assertEqual(12.7, evaluator.lex_parse_eval('(+ 2.7 10)'))
    
    def test_sum(self):
        self.assertEqual(75, evaluator.lex_parse_eval('(+ 21 35 12 7)'))
    
    def test_product(self):
        self.assertEqual(1200, evaluator.lex_parse_eval('(* 25 4 12)'))
    
    def test_nested_arithmetic(self):
        self.assertEqual(19, evaluator.lex_parse_eval('(+ (* 3 5) (- 10 6))'))
    
    def test_var_definition(self):
        evaluator.lex_parse_eval('(define size 2)')
        self.assertEqual(10, evaluator.lex_parse_eval('(* 5 size)'))
    
    def test_mult_definitions(self):
        evaluator.lex_parse_eval('(define pi 3.14159)')
        evaluator.lex_parse_eval('(define radius 10)')
        evaluator.lex_parse_eval('(define circumference (* 2 pi radius))')
        self.assertEqual(62.8318, evaluator.lex_parse_eval('circumference'))
    
    def test_func_definition(self):
        evaluator.lex_parse_eval('(define (square x) (* x x))')
        self.assertEqual(9, evaluator.lex_parse_eval('(square 3)'))
    
    def test_lambda(self):
        evaluator.lex_parse_eval('(define (square x) (* x x))')
        self.assertEqual(12, evaluator.lex_parse_eval('((lambda (x y z) (+ x y (square z))) 1 2 3)'))
    
    def test_cond(self):
        self.assertEqual(2.0, evaluator.lex_parse_eval('(begin (define (abs x) (cond ((> x 0) x) ((= x 0) 0) ((< x 0) (- x)))) (abs -2.0))'))

if __name__ == '__main__':
    unittest.main()