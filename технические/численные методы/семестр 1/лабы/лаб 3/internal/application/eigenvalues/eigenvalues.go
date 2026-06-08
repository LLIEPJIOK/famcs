package eigenvalues

import (
	"fmt"

	"github.com/LLIEPJIOK/eigenvalues/internal/jacobi"
	"github.com/LLIEPJIOK/eigenvalues/internal/matrix"
	"github.com/LLIEPJIOK/eigenvalues/internal/power"
)

func Start() error {
	mtr := matrix.GenerateSymmetricMatrix()

	fmt.Println("Initial matrix:")
	matrix.Print2D(mtr)
	fmt.Println()

	fmt.Println("---Jacobi")

	jacobiResult, err := jacobi.CalcEigenvaluesAndEigenvectors(mtr)
	if err != nil {
		return fmt.Errorf("failed to use jacobi method: %w", err)
	}

	fmt.Printf("Total iterations: %d\n\n", jacobiResult.IterCount)

	for i := range len(jacobiResult.Values) {
		fmt.Printf("eigenvalue #%d: %10.5f\n", i+1, jacobiResult.Values[i])
		fmt.Printf("eigenvector #%d:\n", i+1)
		matrix.Print(jacobiResult.Vectors[i])

		norm, err := matrix.CalcError(mtr, jacobiResult.Vectors[i], jacobiResult.Values[i])
		if err != nil {
			return fmt.Errorf("failed to calculate error: %w", err)
		}

		fmt.Printf("calc error: %e\n\n", norm)
	}

	fmt.Println("---Power")

	powerResult, err := power.CalcEigenvalueAndEigenvector(mtr)
	if err != nil {
		return fmt.Errorf("failed to use power method: %w", err)
	}

	fmt.Printf("Total iterations: %d\n\n", powerResult.IterCount)
	fmt.Printf("eigenvalue: %10.5f\n", powerResult.Value)
	fmt.Printf("eigenvector:\n")
	matrix.Print(powerResult.Vector)

	norm, err := matrix.CalcError(mtr, powerResult.Vector, powerResult.Value)
	if err != nil {
		return fmt.Errorf("failed to calculate error: %w", err)
	}

	fmt.Printf("calc error: %e\n\n", norm)

	return nil
}
