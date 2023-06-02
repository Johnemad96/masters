#!/usr/bin/env python3

import argparse
import numpy as np
# import associate
from orangecontrib.associate import fpgrowth as associate

def align(model, data):
    """Align two trajectories using the method of Horn (closed-form).

    Input:
    model -- first trajectory (3xn)
    data -- second trajectory (3xn)

    Output:
    rot -- rotation matrix (3x3)
    trans -- translation vector (3x1)
    trans_error -- translational error per point (1xn)
    """
    np.set_printoptions(precision=3, suppress=True)
    model_zerocentered = model - model.mean(axis=1, keepdims=True)
    data_zerocentered = data - data.mean(axis=1, keepdims=True)

    W = np.zeros((3, 3))
    for column in range(model.shape[1]):
        W += np.outer(model_zerocentered[:, column], data_zerocentered[:, column])
    U, d, Vh = np.linalg.svd(W.transpose())
    S = np.matrix(np.identity(3))
    if (np.linalg.det(U) * np.linalg.det(Vh)) < 0:
        S[2, 2] = -1
    rot = U * S * Vh
    trans = data.mean(axis=1, keepdims=True) - rot * model.mean(axis=1, keepdims=True)

    model_aligned = rot * model + trans
    alignment_error = model_aligned - data

    trans_error = np.sqrt(np.sum(np.multiply(alignment_error, alignment_error), axis=0)).A[0]

    return rot, trans, trans_error

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first_file", help="first trajectory")
    parser.add_argument("second_file", help="second trajectory")
    parser.add_argument("--offset", help="time offset between the two trajectories (seconds)", default=0.0, type=float)
    parser.add_argument("--scale", help="scaling factor for the second trajectory", default=1.0, type=float)
    parser.add_argument("--max_difference", help="maximally allowed time difference for matching entries (seconds)", default=0.02, type=float)
    parser.add_argument("--plot", help="plot the error over time", default=False, action="store_true")
    args = parser.parse_args()

    first_list = associate.read_file_list(args.first_file)
    second_list = associate.read_file_list(args.second_file)

    matches = associate.associate(first_list, second_list, args.offset, args.max_difference)
    if len(matches) < 2:
        sys.exit("Couldn't find matching timestamp pairs between groundtruth and estimated trajectory! Did you choose the correct sequence?")

    # Read all groundtruth and optimizer poses
    gt = np.ndarray((len(matches), 3))
    opt = np.ndarray((len(matches), 3))
    for i, (first, second) in enumerate(matches):
        gt[i] = first[1:4]
        opt[i] = second[1:4]

    # Scale optimizer trajectory (only scale, not translate)
    if args.scale != 1.0:
        opt *= args.scale

    # Align optimizer pose
    rot, trans, trans_error = align(opt, gt)

    # Calculate ATE statistics
    ate_mean = trans_error.mean()
    ate_median = np.median(trans_error)
    ate_rmse = np.sqrt(np.mean(trans_error ** 2))

    # Print results
    print("Alignment (mean, median, RMSE):\n{:.3f}m, {:.3f}m, {:.3f}m".format(ate_mean, ate_median, ate_rmse))

    # Plot ATE (if requested)
    if args.plot:
        import matplotlib.pyplot as plt
        plt.plot(trans_error)
        plt.title("ATE over time")
        plt.xlabel("Time (frame index)")
        plt.ylabel("Translation error (m)")
        plt.show()

if __name__ == "__main__":
    main()
