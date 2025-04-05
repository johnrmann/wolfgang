// jest.config.ts
import nextJest from 'next/jest.js';

const createJestConfig = nextJest({ dir: './' });

const customJestConfig = {
	testEnvironment: 'jsdom',
	setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
	moduleNameMapper: {
		'^@/components/(.*)$': '<rootDir>/components/$1',
		'^@/core/(.*)$': '<rootDir>/core/$1',
		'^@/api/(.*)$': '<rootDir>/api/$1',
	},
};

export default createJestConfig(customJestConfig);
