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
		Assert.assertEquals(5, calculator.sum(2, 3));
	}

	@Test
	public void SumZero() {
		Assert.assertEquals(0, calculator.sum(0, 0));
		Assert.assertEquals(5, calculator.sum(5, 0)); 
		
	}

	@Test
	public void testSumNegativeNumbers() {
		Assert.assertEquals(-5, calculator.sum(-2, -3));
		Assert.assertEquals(-1, calculator.sum(2, -3));
	}
}
