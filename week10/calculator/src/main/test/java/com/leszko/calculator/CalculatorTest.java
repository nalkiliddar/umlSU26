package com.leszko.calculator;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import static org.junit.jupiter.api.Assertions.assertEquals; 


@SpringBootTest
public class CalculatorTest {

	@Autowired
	private Calculator calculator;

	@Test
	public void SumPositiveNumbers() {
		Assert.assertEquals(7, calculator.sum(2, 5));
	}

	@Test
	public void SumZero() {
		
		Assert.assertEquals(5, calculator.sum(5, 0)); 
		
	}

	@Test
	public void testSumNegativeNumbers() {
		Assert.assertEquals(-7, calculator.sum(-2, -5));
		Assert.assertEquals(-1, calculator.sum(3, -4));
	}
}
