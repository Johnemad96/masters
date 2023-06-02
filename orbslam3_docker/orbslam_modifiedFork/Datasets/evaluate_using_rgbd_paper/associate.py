import numpy as np
import argparse
import associate

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
    model_zerocentered = model - model.mean(1)
    data_zerocentered = data - data.mean(1)

    W = np.zeros((3, 3))
    for column in range(model.shape[1]):
        W += np.outer(model_zerocentered[:, column], data_zerocentered[:, column])
    U, d, Vh = np.linalg.svd(W.transpose())
    S = np.matrix(np.identity(3))
    if (np.linalg.det(U) * np.linalg.det(Vh) < 0):
        S[2, 2] = -1
    rot = U * S * Vh
    trans = data.mean(1) - rot * model.mean(1)

    model_aligned = rot * model + trans
    alignment_error = model_aligned - data

    trans_error = np.sqrt(np.sum(np.multiply(alignment_error, alignment_error), 0)).A[0]

    return rot, trans, trans_error

def compute_ATE(gt, est):
    """Compute the Absolute Trajectory Error (ATE) between ground truth and estimated trajectories.

    Input:
    gt -- ground truth trajectory (3xn)
    est -- estimated trajectory (3xn)

    Output:
    ate -- absolute trajectory error (scalar)
    """
    rot, trans, trans_error = align(gt, est)
    ate = np.mean(trans_error)

    return ate

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("groundtruth_file", help="ground truth file")
    parser.add_argument("estimated_file", help="estimated file")
    parser.add_argument("--plot", help="plot resulting ATE", action='store_true')
    args = parser.parse_args()

    # Load data
    gt_traj = associate.read_file(args.groundtruth_file)
    est_traj = associate.read_file(args.estimated_file)

    # Synchronize data
    matched_traj = associate.associate(gt_traj, est_traj)
    gt_times = np.array([t for (_, t) in matched_traj])
    gt_traj = np.array([x for (x, _) in matched_traj])
    est_traj = np.array([x for (_, x) in matched_traj])

    # Compute Absolute Trajectory Error (ATE)
    ate = compute_ATE(gt_traj, est_traj)
    print(f"ATE: {ate:.3f} m")

    # Compute mean, median, and RMSE of error
    error = np.abs(gt_traj - est_traj)
    mean_error = np.mean(error)
    median_error = np.median(error)
    rmse = np.sqrt(np.mean(np.square(error)))
    print(f"Mean error: {mean_error:.3f} m")
    print(f"Median error: {median_error:.3f} m")
    print(f"RMSE: {rmse:.3f} m")

    # Plot ATE (if requested)
    if args.plot:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Failed to import matplotlib.pyplot, plotting is not available.")
            return

        plt.plot(gt_times, error, 'b', label="Absolute Trajectory Error")
        plt.plot(gt_times, np.ones(len(gt_times)) * ate, 'r', label="ATE Mean")
        plt.plot(gt_times, np.ones(len(gt_times)) * median_error, 'g', label="ATE Median")
        plt.plot(gt_times, np.ones(len(gt_times)) * rmse, 'k', label="ATE RMSE")
        plt.title("Absolute Trajectory Error")
        plt.legend(loc=0, prop={'size':10})
        plt.xlabel("Time (s)")
        plt.ylabel("ATE (m)")
        plt.show()

if __name__ == "__main__":
    main()