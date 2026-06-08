package matrix

import (
	"fmt"
	"math"
)

const (
	MatrixSize = 10
)

func GenerateSymmetricMatrix() [][]float64 {
	mtr := make([][]float64, MatrixSize)

	for i := range MatrixSize {
		mtr[i] = make([]float64, MatrixSize)

		for j := range MatrixSize {
			if i == j {
				mtr[i][j] = 11.0 * math.Sqrt(float64(i+1))
			} else if i < j {
				mtr[i][j] = float64(i+1) / float64(j+1)
			} else {
				mtr[i][j] = mtr[j][i]
			}
		}
	}

	return mtr
}

func CubicNorm(vector []float64) float64 {
	norm := 0.0

	for _, v := range vector {
		norm = max(norm, math.Abs(v))
	}

	return norm
}

func CalcError(mtr [][]float64, eigenvector []float64, eigenvalue float64) (float64, error) {
	left, err := Multiply(mtr, Column(eigenvector...))
	if err != nil {
		return 0, fmt.Errorf("failed to multiply matrices: %w", err)
	}

	norm := 0.0

	for i := range len(left) {
		norm = max(norm, math.Abs(left[i][0]-eigenvalue*eigenvector[i]))
	}

	return norm, nil
}

func Copy(matrix []float64) []float64 {
	matrixCopy := make([]float64, len(matrix))
	copy(matrixCopy, matrix)

	return matrixCopy
}

func Copy2D(matrix [][]float64) [][]float64 {
	matrixCopy := make([][]float64, len(matrix))

	for i := range len(matrix) {
		matrixCopy[i] = Copy(matrix[i])
	}

	return matrixCopy
}

func Print(matrix []float64) {
	for i := range len(matrix) {
		fmt.Printf("%10.5f ", matrix[i])
	}

	fmt.Println()
}

func Print2D(matrix [][]float64) {
	for i := range len(matrix) {
		Print(matrix[i])
	}
}

func Multiply(first, second [][]float64) ([][]float64, error) {
	if len(first[0]) != len(second) {
		return nil, NewErrMatrix("matrices cannot be multiplied")
	}

	mult := make([][]float64, len(first))

	for i := range len(first) {
		mult[i] = make([]float64, len(second[0]))
		for j := range len(second[0]) {
			for k := range len(second) {
				mult[i][j] += first[i][k] * second[k][j]
			}
		}
	}

	return mult, nil
}

func Column(vals ...float64) [][]float64 {
	mtr := make([][]float64, len(vals))
	for i, v := range vals {
		mtr[i] = append(mtr[i], v)
	}

	return mtr
}

func Row(vals ...float64) [][]float64 {
	return [][]float64{vals}
}
