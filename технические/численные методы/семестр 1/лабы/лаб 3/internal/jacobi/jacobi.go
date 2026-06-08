package jacobi

import (
	"fmt"
	"math"

	"github.com/LLIEPJIOK/eigenvalues/internal/matrix"
)

type Result struct {
	Values    []float64
	Vectors   [][]float64
	IterCount int
}

const eps = 1e-5

func sign(numb float64) float64 {
	if numb >= 0 {
		return 1.0
	}

	return -1.0
}

func iteration(mtr [][]float64, i, j int) ([][]float64, [][]float64, error) {
	t := make([][]float64, len(mtr))

	for i := range len(mtr) {
		t[i] = make([]float64, len(mtr))
		t[i][i] = 1
	}

	mu := 2 * mtr[i][j] / (mtr[j][j] - mtr[i][i])
	c := math.Sqrt((1 + 1/math.Sqrt(1+mu*mu)) / 2)
	s := sign(mu) * math.Sqrt((1-1/math.Sqrt(1+mu*mu))/2)

	t[i][i] = c
	t[i][j] = s
	t[j][i] = -s
	t[j][j] = c

	nextMtr, err := matrix.Multiply(mtr, t)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to multiply matrices: %w", err)
	}

	t[i][j], t[j][i] = t[j][i], t[i][j]

	nextMtr, err = matrix.Multiply(t, nextMtr)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to multiply matrices: %w", err)
	}

	t[i][j], t[j][i] = t[j][i], t[i][j]

	return nextMtr, t, nil
}

func CalcEigenvaluesAndEigenvectors(mtr [][]float64) (Result, error) {
	mtr = matrix.Copy2D(mtr)
	t := make([][]float64, len(mtr))
	for i := range len(mtr) {
		t[i] = make([]float64, len(mtr))
		t[i][i] = 1
	}

	iterCount := 0

Iterations:
	for {
		for i := range len(mtr) {
			for j := i + 1; j < len(mtr); j++ {
				if math.Abs(mtr[i][j]) >= eps {
					nextMtr, newT, err := iteration(mtr, i, j)
					if err != nil {
						return Result{}, fmt.Errorf("failed to make iteration: %w", err)
					}

					mtr = nextMtr
					t, err = matrix.Multiply(t, newT)
					if err != nil {
						return Result{}, fmt.Errorf("failed to multiply matrices: %w", err)
					}

					iterCount++
					continue Iterations
				}
			}
		}

		break
	}

	values := make([]float64, len(mtr))

	for i := range len(mtr) {
		values[i] = mtr[i][i]
	}

	vectors := make([][]float64, len(mtr))
	vector := make([]float64, len(mtr))

	for i := range len(mtr) {
		vector[i] = 1
		curVector, err := matrix.Multiply(t, matrix.Column(vector...))
		if err != nil {
			return Result{}, fmt.Errorf("failed to multiply matrices: %w", err)
		}

		vectors[i] = make([]float64, len(mtr))
		for j := range len(mtr) {
			vectors[i][j] = curVector[j][0]
		}

		vector[i] = 0
	}

	return Result{
		Values:    values,
		Vectors:   vectors,
		IterCount: iterCount,
	}, nil
}
