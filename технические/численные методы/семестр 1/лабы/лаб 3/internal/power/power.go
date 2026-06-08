package power

import (
	"fmt"

	"github.com/LLIEPJIOK/eigenvalues/internal/matrix"
)

type Result struct {
	Value     float64
	Vector    []float64
	IterCount int
}

const eps = 1e-5

func CalcEigenvalueAndEigenvector(mtr [][]float64) (Result, error) {
	u := make([]float64, len(mtr))
	u[0] = 1
	id, iterCount := 0, 0

	for {
		iterCount++

		y, err := matrix.Multiply(mtr, matrix.Column(u...))
		if err != nil {
			return Result{}, fmt.Errorf("failed to multiply matrices: %w", err)
		}

		lambda := y[id][0] / u[id]

		for i := range u {
			u[i] = y[i][0]
		}

		norm := matrix.CubicNorm(u)
		for i := range u {
			u[i] /= norm
			if u[i] == 1 {
				id = i
			}
		}

		calcError, err := matrix.CalcError(mtr, u, lambda)
		if err != nil {
			return Result{}, fmt.Errorf("failed to calculate error: %w", err)
		}

		if calcError < eps {
			return Result{
				Value:     lambda,
				Vector:    u,
				IterCount: iterCount,
			}, nil
		}
	}
}
