package com.leszko.calculator;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import static org.assertj.core.api.Assertions.assertThat;

/** Test for Calculator logic */
@SpringBootTest
public class CalculatorTest {

	@Autowired
	private Calculator calculator;

	@Test
	public void testSumPositiveNumbers() {
		assertThat(calculator.sum(2, 3)).isEqualTo(5);
	}

	@Test
	public void testSumZero() {
		assertThat(calculator.sum(0, 0)).isEqualTo(0);
		assertThat(calculator.sum(5, 0)).isEqualTo(10);
	}

	@Test
	public void testSumNegativeNumbers() {
		assertThat(calculator.sum(-2, -3)).isEqualTo(-5);
		assertThat(calculator.sum(2, -3)).isEqualTo(-1);
	}
}
