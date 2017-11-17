#ifndef CalibCalorimetry_EcalWeightsTools_ComputeWeights_h
#define CalibCalorimetry_EcalWeightsTools_ComputeWeights_h

/** \class ComputeWeights
  *  Class used to compute weights from a pulse shape profile.
  *
  *  $Date: 2009/10/12 13:04:29 $
  *  $Revision: 1.3 $
  *  \author R. Bruneliere - CERN
  */

// Looked at by Abe Tishelman-Charny on 8, November 2017

// Math header files.

#include <vector>

// Other Header Files

#include "CLHEP/Matrix/Matrix.h"
#include "CLHEP/Matrix/SymMatrix.h"

// #include "/home/abe/Documents/Fall_2017/Computational_Physics/CLHEP/Matrix/Matrix/Matrix.h"
// #include "/home/abe/Documents/Fall_2017/Computational_Physics/CLHEP/Matrix/Matrix/SymMatrix.h"

class ComputeWeights
{
 
 // Can access outside of class
 public:
  /// Constructor
  // explicit ComputeWeights(edm::ParameterSet const& pSet);
  ComputeWeights(int verbosity, bool doFitBaseline, bool doFitTime, 
		 int nPulseSamples, int nPrePulseSamples);

  /// Destructor
  ~ComputeWeights();

  /// Compute weights from an input pulse shape
  bool compute(const std::vector<double>& pulseShape,
	       const std::vector<double>& pulseShapeDerivative,
	       const double tMax); //modif

  /// Get weight used to compute amplitude
  double getAmpWeight(int iSample) const;

  /// Get weight used to compute dynamic pedestal
  double getPedWeight(int iSample) const;

  /// Get weight used to compute time jitter
  double getTimeWeight(int iSample) const;

  /// Get chi2 matrix
  double getChi2Matrix(int iSample1, int iSample2) const;

 // Only accessible through class methods 
 private:
  int verbosity_;        //< Messages verbosity
  bool doFitBaseline_;   //< Fit baseline or not
  bool doFitTime_;       //< Fit time jitter or not
  int nPulseSamples_;    //< Number of samples in the pulse
  int nPrePulseSamples_; //< Number of samples in the pre-pulse
  CLHEP::HepMatrix weights_; // Namesapce CLHEP, class HepMatrix, instance (function?) 'weights'
  CLHEP::HepSymMatrix chi2_;

};
#endif // CalibCalorimetry_EcalWeightsTools_ComputeWeights_h
