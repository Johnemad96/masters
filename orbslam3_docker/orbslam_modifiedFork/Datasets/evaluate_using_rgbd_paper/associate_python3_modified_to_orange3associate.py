#!/usr/bin/env python3
import sys
import argparse
import numpy as np
from orangecontrib.associate.fpgrowth import *

def read_file_list(file_name):
    file_list = []
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            if len(line)>0:
                line_parts = line.split()
                file_list.append((float(line_parts[0]),line_parts[1:]))
    return file_list
def associate(first_list, second_list, max_difference):
    first_list_index = 0
    second_list_index = 0
    matches = []
    while first_list_index < len(first_list) and second_list_index < len(second_list):
        first_stamp = first_list[first_list_index][0]
        second_stamp = second_list[second_list_index][0]
        time_difference = second_stamp - first_stamp
        if abs(time_difference) < max_difference:
            matches.append((first_list_index, second_list_index))
            first_list_index += 1
            second_list_index += 1
        elif time_difference > 0:
            second_list_index += 1
        else:
            first_list_index += 1
    return matches
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
    model_zerocentered = model - model.mean(1)
    data_zerocentered = data - data.mean(1)
    
    W = np.zeros((3, 3))
    for column in range(model.shape[1]):
        W += np.outer(model_zerocentered[:, column], data_zerocentered[:, column])
    U, d, Vh = np.linalg.linalg.svd(W.transpose())
    S = np.matrix(np.identity(3))
    if (np.linalg.det(U) * np.linalg.det(Vh)) < 0:
        S[2, 2] = -1
    rot = U * S * Vh
    trans = data.mean(1) - rot * model.mean(1)
    
    model_aligned = rot * model + trans
    alignment_error = model_aligned - data
    
    trans_error = np.sqrt(np.sum(np.multiply(alignment_error, alignment_error), 0)).A[0]
        
    return rot, trans, trans_error

def plot_traj(ax, stamps, traj, style, color, label):
    """
    Plot a trajectory using matplotlib. 
    
    Input:
    ax -- the plot
    stamps -- time stamps (1xn)
    traj -- trajectory (3xn)
    style -- line style
    color -- line color
    label -- plot legend
    
    """
    stamps.sort()
    interval = np.median([s-t for s,t in zip(stamps[1:],stamps[:-1])])
    x = []
    y = []
    last = stamps[0]
    for i in range(len(stamps)):
        if stamps[i]-last < 2*interval:
            x.append(traj[i][0])
            y.append(traj[i][1])
        elif len(x)>0:
            ax.plot(x, y, style, color=color, label=label)
            label=""
            x=[]
            y=[]
        last= stamps[i]
    if len(x)>0:
        ax.plot(x, y, style, color=color, label=label)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first_file", help="input file")
    parser.add_argument("second_file", help="input file")
    parser.add_argument("--plot", help="plot the aligned trajectories", action="store_true")
    parser.add_argument("--scale", help="scale the trajectories (works only with 2D)", action="store_true")
    parser.add_argument("--max_difference", help="maximally allowed time diffrence for matching entries (default: 0.02)",default=0.02,type=float)
    parser.add_argument("--offset", help="time offset for second trajectory (default: 0)",default=0,type=float)
    parser.add_argument("--save_plot", help="save plot instead of showing it")
    parser.add_argument("--only_scale", help="only scale, do not translate", action="store_true")
    args = parser.parse_args()
    
    # Read all groundtruth and optimizer poses
    first_list = read_file_list(args.first_file)
    second_list = read_file_list(args.second_file)
    
    # Associate the two sets of poses based on their timestamps
    matches = associate(first_list, second_list,float(args.max_difference))
    if len(matches)<2:
        sys.exit("Couldn't find matching timestamp pairs between groundtruth and optimizer. Did you choose the correct sequence?")
    
    first_xyz = np.matrix([[float(value) for value in first_list[a][0:3]] for a,b in matches]).transpose()
    second_xyz = np.matrix([[float(value) for value in second_list[b][0:3]] for a,b in matches]).transpose()
    
    if args.only_scale:
        # Scale optimizer trajectory (only scale, not translate)
        second_xyz[0:2] = second_xyz[0:2] * (np.mean(first_xyz[0:2]) / np.mean(second_xyz[0:2]))
    else:
        # Find the scale and translation to align the two trajectories
        rot, trans, trans_error = align(second_xyz, first_xyz)
        second_xyz = rot * second_xyz + trans
        
    # Compute absolute trajectory error
    ate = np.sqrt(np.sum(np.multiply(first_xyz - second_xyz, first_xyz - second_xyz), 0)).A[0]
    mean_ate = np.mean(ate)
    std_ate = np.std(ate)
    median_ate = np.median(ate)
    rmse_ate = np.sqrt(np.mean(np.multiply(ate, ate)))

    print("ATE: %.2f +/- %.2f m (mean +/- std)" % (mean_ate, std_ate))
    print("Median ATE: %.2f m" % median_ate)
    print("RMSE ATE: %.2f m" % rmse_ate)

    if args.plot:
        # Plot ATE (if requested)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(np.array(range(len(ate))), ate, "r", label="ATE")
        plt.plot(np.array(range(len(ate))), np.ones(len(ate))*mean_ate, "g", label="mean ATE = %.2f m" % mean_ate)
        plt.plot(np.array(range(len(ate))), np.ones(len(ate))*median_ate, "b", label="median ATE = %.2f m" % median_ate)
        plt.plot(np.array(range(len(ate))), np.ones(len(ate))*rmse_ate, "c", label="RMSE ATE = %.2f m" % rmse_ate)
        plt.legend()
        plt.xlabel("Frame")
        plt.ylabel("ATE (m)")
        if args.save_plot:
            plt.savefig(args.save_plot)
        else:
            plt.show()

if __name__ == "__main__":
    main()


