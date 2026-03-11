import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Flow Data Analysis", layout="wide")

# Title
st.title("Event Threshold App - Version 1.0")

st.markdown("Please make sure the title is 'Date' and 'Flow' in the uploaded CSV file (It is case sensitive).")

st.markdown(
    "[see Help interface for date formatting](https://event-package-website.web.app/help)",
    unsafe_allow_html=True
)

# File uploader
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# Initialize variables
df = None
error_message = ""
success_message = ""

# Check uploaded file
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        # Verify column names
        if list(df.columns)[:2] == ["Date", "Flow"]:
            success_message = "File uploaded successfully!"
            # Display first 50 lines
            st.subheader("Preview of Uploaded File (First 50 Rows)")
            st.dataframe(df.head(51), use_container_width=True)
        else:
            error_message = "Error: CSV must have 'Date' as first column and 'Flow' as second column"
    except Exception as e:
        error_message = f"Error reading CSV file: {str(e)}"

# Display messages
if success_message:
    st.success(success_message)
if error_message:
    st.error(error_message)

# Initialize session state for toggles
if 'time_scale' not in st.session_state:
    st.session_state.time_scale = 'Daily'
if 'seasonal_delineation' not in st.session_state:
    st.session_state.seasonal_delineation = 'A'

# Toggle button for time scale
time_scale = st.radio(
    "Select Analysis Time Scale",
    ['Daily', 'Hourly'],
    index=0 if st.session_state.time_scale == 'Daily' else 1,
    horizontal=True
)
st.session_state.time_scale = time_scale

# Toggle button for seasonal delineation
seasonal_delineation = st.radio(
    "Select Seasonal Delineation",
    ['A', 'B'],
    index=0 if st.session_state.seasonal_delineation == 'A' else 1,
    horizontal=True
)
st.session_state.seasonal_delineation = seasonal_delineation


if time_scale == 'Daily':
    baseflow_amp_factor_WS = st.slider(
        "Baseflow Amplification Factor (Winter/Spring Threshold Multiplier)",
        min_value=0.01,
        max_value=10.00,
        value=1.5,
        step=0.01
    )
    st.session_state.baseflow_amp_factor_WS = baseflow_amp_factor_WS


    baseflow_amp_factor_SF = st.slider(
        "Baseflow Amplification Factor (Summer/Fall Threshold Multiplier)",
        min_value=0.01,
        max_value=10.00,
        value=2.0,
        step=0.01
    )
    st.session_state.baseflow_amp_factor_SF = baseflow_amp_factor_SF

    # flashiness = 1.25
    flashiness = st.slider(
        "flashiness",
        min_value=0.0,
        max_value=2.00,
        value=1.25,
        step=0.01
    )
    st.session_state.flashiness = flashiness

else:
    baseflow_amp_factor_WS = st.slider(
        "Baseflow Amplification Factor (Winter/Spring Threshold Multiplier)",
        min_value=0.01,
        max_value=10.00,
        value=3.0,
        step=0.01
    )
    st.session_state.baseflow_amp_factor_WS = baseflow_amp_factor_WS


    baseflow_amp_factor_SF = st.slider(
        "Baseflow Amplification Factor (Summer/Fall Threshold Multiplier)",
        min_value=0.01,
        max_value=10.00,
        value=3.5,
        step=0.01
    )
    st.session_state.baseflow_amp_factor_SF = baseflow_amp_factor_SF

    # flashiness = 1.25
    flashiness = st.slider(
        "flashiness",
        min_value=0.0,
        max_value=2.00,
        value=1.25,
        step=0.01
    )
    st.session_state.flashiness = flashiness

# if time_scale == 'Daily':
#     st.info("Recommendation: Minimum of 1 year data required for daily analysis")
# else:
#     st.info("Recommendation: Minimum of 3 months data required for hourly analysis")

# Run analysis button
run_analysis = st.button("Run Analysis")

# Output area
if run_analysis:
    if df is None:
        st.error("Please upload a CSV file before running the analysis.")
    elif error_message:
        st.error(error_message)
    else:
        try:
            winter = []
            spring = []
            summer = []
            fall = []
            # Convert Date to datetime
            
            df['Date'] = pd.to_datetime(df['Date'])
            df["month"] = df["Date"].dt.month
            for elements in range(0, len(df['month'])):
#                     print(type(elements))
                if seasonal_delineation == "A":
                    if df['month'][elements] == 1 or  df['month'][elements] == 2 or df['month'][elements] == 3:
                        winter.append(float(df['Flow'][elements]))
                    elif df['month'][elements] == 4 or  df['month'][elements] == 5 or df['month'][elements] == 6:
                        spring.append(float(df['Flow'][elements]))
                    elif df['month'][elements] == 7  or  df['month'][elements] == 8 or df['month'][elements] == 9:
                        summer.append(float(df['Flow'][elements]))
                    else:
                        fall.append(float(df['Flow'][elements]))
                        
                else:
                    if df['month'][elements] == 1 or  df['month'][elements] == 2 or df['month'][elements] == 12:
                        winter.append(float(df['Flow'][elements]))
                    elif df['month'][elements] == 4 or  df['month'][elements] == 5 or df['month'][elements] == 3:
                        spring.append(float(df['Flow'][elements]))
                    elif df['month'][elements] == 7  or  df['month'][elements] == 8 or df['month'][elements] == 6:
                        summer.append(float(df['Flow'][elements]))
                    else:
                        fall.append(float(df['Flow'][elements]))
#                 print('Date')
#                 print(df['Date'])
#                 print('\n')
#                 print('Flow')
#                 print(df['Flow'])
            
#                 print(winter)
#                 print(spring)
#                 print(summer)
#                 print(fall)
                





            if len(winter) > 0:
                st.header("Winter Analysis")
#                     print(winter)
#                     print(type(winter[0]))
                data = winter
                
                # Create DataFrame
                df = pd.DataFrame(data, columns=["flow"])

                # Calculate quartiles and other quantiles\
                
                ## this is the point of the code where youc an change the percentage of the threshold

                #Winter Lyne and Hollick filter
                
                a = df["flow"].fillna(0).tolist()

                # a = df["flow"].tolist()
                bass_river_flow = np.array(a)
                # --------------------------
                # Padding
                # --------------------------
                def _reflect_pad_30(q):
                    left = q[1:31][::-1]
                    right = q[-31:-1][::-1]
                    return np.concatenate([left, q, right])


                # --------------------------
                # Single Lyne-Hollick pass
                # --------------------------
                def _lh_single_pass(q_in, alpha, direction, qf0):
                    n = len(q_in)
                    qf = np.empty(n, dtype=float)

                    if direction == 1:
                        qf[0] = qf0
                        for i in range(1, n):
                            qf[i] = alpha * qf[i - 1] + (1 + alpha) / 2.0 * (q_in[i] - q_in[i - 1])
                    else:
                        qf[-1] = qf0
                        for i in range(n - 2, -1, -1):
                            qf[i] = alpha * qf[i + 1] + (1 + alpha) / 2.0 * (q_in[i] - q_in[i + 1])

                    qb = q_in - qf
                    qb = np.clip(qb, 0.0, q_in)
                    return qb


                # --------------------------
                # Standardized LH (Ladson)
                # --------------------------
                def lyne_hollick_ladson(q, alpha=0.925, passes=3, pad_n=30):
                    q = np.asarray(q, dtype=float)
                    qp = _reflect_pad_30(q)
                    dirs = [1 if (k % 2 == 0) else -1 for k in range(passes)]

                    qb_prev = None
                    q_in = qp

                    for k, d in enumerate(dirs):
                        if k == 0:
                            qf0 = q_in[0] if d == 1 else q_in[-1]
                        else:
                            q_in = qb_prev
                            qf0 = qb_prev[-1] if d == -1 else qb_prev[0]

                        qb_prev = _lh_single_pass(q_in=q_in, alpha=alpha, direction=d, qf0=qf0)

                    qb = qb_prev[pad_n:-pad_n]
                    bfi = float(np.sum(qb) / np.sum(q))
                    return qb, bfi


                # --------------------------
                # Alpha sensitivity
                # --------------------------
                def alpha_sensitivity(q, alphas, passes=3):
                    results = []
                    for a in alphas:
                        _, bfi = lyne_hollick_ladson(q=q, alpha=float(a), passes=passes)
                        results.append((float(a), bfi))
                    return results


                # --------------------------
                # Knee selection
                # --------------------------
                def select_alpha_knee(alphas, bfis):
                    x = np.asarray(alphas, dtype=float)
                    y = np.asarray(bfis, dtype=float)

                    p0 = np.array([x[0], y[0]])
                    p1 = np.array([x[-1], y[-1]])
                    v = p1 - p0
                    v_norm = np.linalg.norm(v)

                    dists = []
                    for xi, yi in zip(x, y):
                        p = np.array([xi, yi])
                        dist = np.linalg.norm(np.cross(v, p - p0)) / v_norm
                        dists.append(dist)

                    return int(np.argmax(dists))


                # --------------------------
                # Run + plot
                # --------------------------
                alphas_grid = np.linspace(0.90, 0.99, 100)
                results = alpha_sensitivity(q=bass_river_flow, alphas=alphas_grid)

                alphas = [r[0] for r in results]
                bfis = [r[1] for r in results]

                idx = select_alpha_knee(alphas, bfis)
                alpha_star = alphas[idx]
                bfi_star = bfis[idx]
                # print(f'This is the winter threshold {bfi_star}')


                percentile_list = []
                percent_sum = []
                # print(a)
                for elements in a:
                    if float(elements) > 0:
                        # print(type(elements))
                        percentile_list.append(round(float(elements), 2))
                # print(np.mean(percentile_list))
                

                if time_scale == 'Daily':
                    def frequency_weighted_mean(percentile_list):

                        percentile_list = np.array(percentile_list, dtype=float)

                        unique, counts = np.unique(percentile_list, return_counts=True)

                        freq_dict = dict(zip(unique, counts))

                        weights = np.array([1 / freq_dict[x] for x in percentile_list])

                        return np.sum(percentile_list * weights) / np.sum(weights)

                    percentile_list = np.round(percentile_list, 2)                   
                    chosen_threshold = frequency_weighted_mean(percentile_list)

                else:
                    chosen_threshold = np.mean(percentile_list)     
                # print(f'This is the bfi for winter {bfi_star}')


                # plt.figure()
                # plt.plot(alphas, bfis)
                # plt.scatter([alpha_star], [bfi_star])

                # plt.annotate(
                #     f"Selected (knee)\nalpha={alpha_star:.3f}\nBFI={bfi_star:.3f}",
                #     xy=(alpha_star, bfi_star),
                #     xytext=(10, 10),
                #     textcoords="offset points"
                # )

                # plt.xlabel("alpha")
                # plt.ylabel("BFI")
                # plt.title("BFI sensitivity to alpha (knee selection)")
                # plt.show()

                # print(f"Knee-selected alpha={alpha_star:.3f}, BFI={bfi_star:.3f}")
                
                # chosen_quantile *= 2
                
                quantiles = {
                    "Q1 (25th Percentile)": df["flow"].quantile(0.25),
                    "Q2 (Median, 50th Percentile)": df["flow"].quantile(0.50),
                    "Q3 (75th Percentile)": df["flow"].quantile(0.75),
                    "80th Percentile": df["flow"].quantile(0.80),
                    # "threshold Percentile": baseflow_amp_factor_WS * 1.25 * chosen_threshold
                    "threshold Percentile": st.session_state.baseflow_amp_factor_WS * flashiness * chosen_threshold * bfi_star,
                    # "threshold Percentile": df["flow"].quantile(0.825),
                    "85th Percentile": df["flow"].quantile(0.85)
                }

                # print('These are the Quantiles')
                # print("Quantiles:")
                # for key, value in quantiles.items():
                #     print(f"{key}: {value:.4f}")

                # Calculate additional statistics
                stats = {
                    "Mean": df["flow"].mean(),
                    "Std": df["flow"].std(),
                    "Min": df["flow"].min(),
                    "Max": df["flow"].max(),
                    "IQR": quantiles["Q3 (75th Percentile)"] - quantiles["Q1 (25th Percentile)"],
                    "Outlier Threshold (Q3 + 1.5*IQR)": quantiles["Q3 (75th Percentile)"] + 1.5 * (quantiles["Q3 (75th Percentile)"] - quantiles["Q1 (25th Percentile)"])
                }
                # print("\nAdditional Statistics:")
                # for key, value in stats.items():
                #     print(f"{key}: {value:.4f}")

                # Apply threshold for high/low flow
                threshold = quantiles["threshold Percentile"]
                if threshold < 0.01 and time_scale == 'Hourly':
                    threshold = 0.01

                if threshold < 0.15 and time_scale == 'Daily':
                    threshold = 0.2


                df["flow_type"] = df["flow"].apply(lambda x: "High" if x > threshold else "Low")
                high_count = len(df[df["flow_type"] == "High"])
                low_count = len(df[df["flow_type"] == "Low"])
#                     print(f"\nThreshold: {threshold}")
                # print(f"High flow count (> {threshold}): {high_count}")
                # print(f"Low flow count (≤ {threshold}): {low_count}")

                # Create a figure with subplots
                plt.figure(figsize=(15, 10))

                # 1. Histogram
                plt.subplot(2, 2, 1)
                sns.histplot(df["flow"], bins=20, kde=False)
                plt.axvline(x=quantiles["Q1 (25th Percentile)"], color="green", linestyle="--", label="Q1")
                plt.axvline(x=quantiles["Q2 (Median, 50th Percentile)"], color="blue", linestyle="--", label="Q2 (Median)")
                plt.axvline(x=quantiles["Q3 (75th Percentile)"], color="orange", linestyle="--", label="Q3")
                plt.axvline(x=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("Histogram of Flow Values with Quartiles")
                plt.xlabel("Flow Value")
                plt.ylabel("Frequency")
                plt.legend()

                # 2. Box Plot
                plt.subplot(2, 2, 2)
                sns.boxplot(y=df["flow"])
                plt.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("Box Plot of Flow Values")
                plt.ylabel("Flow Value")
                plt.legend()

                # 3. KDE Plot
                plt.subplot(2, 2, 3)
                sns.kdeplot(df["flow"], fill=True)
                plt.axvline(x=quantiles["Q1 (25th Percentile)"], color="green", linestyle="--", label="Q1")
                plt.axvline(x=quantiles["Q2 (Median, 50th Percentile)"], color="blue", linestyle="--", label="Q2 (Median)")
                plt.axvline(x=quantiles["Q3 (75th Percentile)"], color="orange", linestyle="--", label="Q3")
                plt.axvline(x=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("KDE Plot of Flow Values with Quartiles")
                plt.xlabel("Flow Value")
                plt.ylabel("Density")
                plt.legend()

                # 4. Time Series Plot
                plt.subplot(2, 2, 4)
                plt.plot(df.index, df["flow"], label="Flow Values", marker="o")
                plt.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                high_flow = df[df["flow_type"] == "High"]
                plt.scatter(high_flow.index, high_flow["flow"], color="red", label="High Flow", zorder=5)
                plt.title("Time Series of Flow Values with Threshold")
                plt.xlabel("Index")
                plt.ylabel("Flow Value")
                plt.legend()
                plt.grid(True)

                # Adjust layout and display
                plt.tight_layout()
                plt.show()
                st.pyplot(plt)

                # Display first few rows of the DataFrame
                # print("\nDataFrame with Flow Classification:")
                # print(df.head(10))
                threshold1 = threshold
                winter_threshold = threshold1
            else:
                st.write("No data available for Winter analysis.")
                threshold1 = 0
                winter_threshold = threshold1
                


















            if len(spring) > 0:
                st.header("Spring Analysis")
#                     print(spring)
                data = spring
                
                # Create DataFrame
                df = pd.DataFrame(data, columns=["flow"])

                # Calculate quartiles and other quantiles

                #Spring Lyne and Hollick filter
                
                a = df["flow"].fillna(0).tolist()

                # a = df["flow"].tolist()
                bass_river_flow = np.array(a)
                # --------------------------
                # Padding
                # --------------------------
                def _reflect_pad_30(q):
                    left = q[1:31][::-1]
                    right = q[-31:-1][::-1]
                    return np.concatenate([left, q, right])


                # --------------------------
                # Single Lyne-Hollick pass
                # --------------------------
                def _lh_single_pass(q_in, alpha, direction, qf0):
                    n = len(q_in)
                    qf = np.empty(n, dtype=float)

                    if direction == 1:
                        qf[0] = qf0
                        for i in range(1, n):
                            qf[i] = alpha * qf[i - 1] + (1 + alpha) / 2.0 * (q_in[i] - q_in[i - 1])
                    else:
                        qf[-1] = qf0
                        for i in range(n - 2, -1, -1):
                            qf[i] = alpha * qf[i + 1] + (1 + alpha) / 2.0 * (q_in[i] - q_in[i + 1])

                    qb = q_in - qf
                    qb = np.clip(qb, 0.0, q_in)
                    return qb


                # --------------------------
                # Standardized LH (Ladson)
                # --------------------------
                def lyne_hollick_ladson(q, alpha=0.925, passes=3, pad_n=30):
                    q = np.asarray(q, dtype=float)
                    qp = _reflect_pad_30(q)
                    dirs = [1 if (k % 2 == 0) else -1 for k in range(passes)]

                    qb_prev = None
                    q_in = qp

                    for k, d in enumerate(dirs):
                        if k == 0:
                            qf0 = q_in[0] if d == 1 else q_in[-1]
                        else:
                            q_in = qb_prev
                            qf0 = qb_prev[-1] if d == -1 else qb_prev[0]

                        qb_prev = _lh_single_pass(q_in=q_in, alpha=alpha, direction=d, qf0=qf0)

                    qb = qb_prev[pad_n:-pad_n]
                    bfi = float(np.sum(qb) / np.sum(q))
                    return qb, bfi


                # --------------------------
                # Alpha sensitivity
                # --------------------------
                def alpha_sensitivity(q, alphas, passes=3):
                    results = []
                    for a in alphas:
                        _, bfi = lyne_hollick_ladson(q=q, alpha=float(a), passes=passes)
                        results.append((float(a), bfi))
                    return results


                # --------------------------
                # Knee selection
                # --------------------------
                def select_alpha_knee(alphas, bfis):
                    x = np.asarray(alphas, dtype=float)
                    y = np.asarray(bfis, dtype=float)

                    p0 = np.array([x[0], y[0]])
                    p1 = np.array([x[-1], y[-1]])
                    v = p1 - p0
                    v_norm = np.linalg.norm(v)

                    dists = []
                    for xi, yi in zip(x, y):
                        p = np.array([xi, yi])
                        dist = np.linalg.norm(np.cross(v, p - p0)) / v_norm
                        dists.append(dist)

                    return int(np.argmax(dists))


                # --------------------------
                # Run + plot
                # --------------------------
                alphas_grid = np.linspace(0.90, 0.99, 100)
                results = alpha_sensitivity(q=bass_river_flow, alphas=alphas_grid)

                alphas = [r[0] for r in results]
                bfis = [r[1] for r in results]

                idx = select_alpha_knee(alphas, bfis)
                alpha_star = alphas[idx]
                bfi_star = bfis[idx]
                # print(f'This is the spring threshold {bfi_star}')

                percentile_list = []
                percent_sum = []
                # print(a)
                for elements in a:
                    if float(elements) > 0:
                        percentile_list.append(elements)
                # print(np.mean(percentile_list))
                # print(percentile_list)
                
                if time_scale == 'Daily':
                    def frequency_weighted_mean(percentile_list):

                        percentile_list = np.array(percentile_list, dtype=float)

                        unique, counts = np.unique(percentile_list, return_counts=True)

                        freq_dict = dict(zip(unique, counts))

                        weights = np.array([1 / freq_dict[x] for x in percentile_list])

                        return np.sum(percentile_list * weights) / np.sum(weights)

                    percentile_list = np.round(percentile_list, 2)              
                    chosen_threshold = frequency_weighted_mean(percentile_list)
                    # print('This is the chosen')
                    # print(chosen_threshold)
                else:
                    chosen_threshold = np.mean(percentile_list)
                # print(f'This is the bfi for spring {bfi_star}')


                # plt.figure()
                # plt.plot(alphas, bfis)
                # plt.scatter([alpha_star], [bfi_star])

                # plt.annotate(
                #     f"Selected (knee)\nalpha={alpha_star:.3f}\nBFI={bfi_star:.3f}",
                #     xy=(alpha_star, bfi_star),
                #     xytext=(10, 10),
                #     textcoords="offset points"
                # )

                # plt.xlabel("alpha")
                # plt.ylabel("BFI")
                # plt.title("BFI sensitivity to alpha (knee selection)")
                # plt.show()

                # print(f"Knee-selected alpha={alpha_star:.3f}, BFI={bfi_star:.3f}")
                # chosen_quantile *= 2
                
                quantiles = {
                    "Q1 (25th Percentile)": df["flow"].quantile(0.25),
                    "Q2 (Median, 50th Percentile)": df["flow"].quantile(0.50),
                    "Q3 (75th Percentile)": df["flow"].quantile(0.75),
                    "80th Percentile": df["flow"].quantile(0.80),
                    "threshold Percentile": st.session_state.baseflow_amp_factor_WS * flashiness * chosen_threshold * bfi_star,
                    # "threshold Percentile": df["flow"].quantile(0.825),
                    "85th Percentile": df["flow"].quantile(0.85)
                }

                # print('These are the Quantiles')
                # print("Quantiles:")
                # for key, value in quantiles.items():
                #     print(f"{key}: {value:.4f}")

                # Calculate additional statistics
                stats = {
                    "Mean": df["flow"].mean(),
                    "Std": df["flow"].std(),
                    "Min": df["flow"].min(),
                    "Max": df["flow"].max(),
                    "IQR": quantiles["Q3 (75th Percentile)"] - quantiles["Q1 (25th Percentile)"],
                    "Outlier Threshold (Q3 + 1.5*IQR)": quantiles["Q3 (75th Percentile)"] + 1.5 * (quantiles["Q3 (75th Percentile)"] - quantiles["Q1 (25th Percentile)"])
                }
                # print("\nAdditional Statistics:")
                # for key, value in stats.items():
                #     print(f"{key}: {value:.4f}")

                # Apply threshold for high/low flow
                threshold = quantiles["threshold Percentile"]
                if threshold < 0.01 and time_scale == 'Hourly':
                    threshold = 0.01

                if threshold < 0.15 and time_scale == 'Daily':
                    threshold = 0.2

                df["flow_type"] = df["flow"].apply(lambda x: "High" if x > threshold else "Low")
                high_count = len(df[df["flow_type"] == "High"])
                low_count = len(df[df["flow_type"] == "Low"])
#                     print(f"\nThreshold: {threshold}")
                # print(f"High flow count (> {threshold}): {high_count}")
                # print(f"Low flow count (≤ {threshold}): {low_count}")

                # Create a figure with subplots
                plt.figure(figsize=(15, 10))

                # 1. Histogram
                plt.subplot(2, 2, 1)
                sns.histplot(df["flow"], bins=20, kde=False)
                plt.axvline(x=quantiles["Q1 (25th Percentile)"], color="green", linestyle="--", label="Q1")
                plt.axvline(x=quantiles["Q2 (Median, 50th Percentile)"], color="blue", linestyle="--", label="Q2 (Median)")
                plt.axvline(x=quantiles["Q3 (75th Percentile)"], color="orange", linestyle="--", label="Q3")
                plt.axvline(x=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("Histogram of Flow Values with Quartiles")
                plt.xlabel("Flow Value")
                plt.ylabel("Frequency")
                plt.legend()

                # 2. Box Plot
                plt.subplot(2, 2, 2)
                sns.boxplot(y=df["flow"])
                plt.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("Box Plot of Flow Values")
                plt.ylabel("Flow Value")
                plt.legend()

                # 3. KDE Plot
                plt.subplot(2, 2, 3)
                sns.kdeplot(df["flow"], fill=True)
                plt.axvline(x=quantiles["Q1 (25th Percentile)"], color="green", linestyle="--", label="Q1")
                plt.axvline(x=quantiles["Q2 (Median, 50th Percentile)"], color="blue", linestyle="--", label="Q2 (Median)")
                plt.axvline(x=quantiles["Q3 (75th Percentile)"], color="orange", linestyle="--", label="Q3")
                plt.axvline(x=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("KDE Plot of Flow Values with Quartiles")
                plt.xlabel("Flow Value")
                plt.ylabel("Density")
                plt.legend()

                # 4. Time Series Plot
                plt.subplot(2, 2, 4)
                plt.plot(df.index, df["flow"], label="Flow Values", marker="o")
                plt.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                high_flow = df[df["flow_type"] == "High"]
                plt.scatter(high_flow.index, high_flow["flow"], color="red", label="High Flow", zorder=5)
                plt.title("Time Series of Flow Values with Threshold")
                plt.xlabel("Index")
                plt.ylabel("Flow Value")
                plt.legend()
                plt.grid(True)

                # Adjust layout and display
                plt.tight_layout()
                plt.show()
                st.pyplot(plt)

                # Display first few rows of the DataFrame
                # print("\nDataFrame with Flow Classification:")
                # print(df.head(10))
                threshold2 = threshold
                spring_threshold = threshold2
            else:
                st.write("No data available for Spring analysis.")
                threshold2 = 0
                spring_threshold = threshold2
                


















            if len(summer) > 0:
                st.header("Summer Analysis")
                data = summer
                
                # Create DataFrame
                df = pd.DataFrame(data, columns=["flow"])

                #Summer Lyne and Hollick filter
                
                a = df["flow"].fillna(0).tolist()

                # a = df["flow"].tolist()
                bass_river_flow = np.array(a)
                # --------------------------
                # Padding
                # --------------------------
                def _reflect_pad_30(q):
                    left = q[1:31][::-1]
                    right = q[-31:-1][::-1]
                    return np.concatenate([left, q, right])


                # --------------------------
                # Single Lyne-Hollick pass
                # --------------------------
                def _lh_single_pass(q_in, alpha, direction, qf0):
                    n = len(q_in)
                    qf = np.empty(n, dtype=float)

                    if direction == 1:
                        qf[0] = qf0
                        for i in range(1, n):
                            qf[i] = alpha * qf[i - 1] + (1 + alpha) / 2.0 * (q_in[i] - q_in[i - 1])
                    else:
                        qf[-1] = qf0
                        for i in range(n - 2, -1, -1):
                            qf[i] = alpha * qf[i + 1] + (1 + alpha) / 2.0 * (q_in[i] - q_in[i + 1])

                    qb = q_in - qf
                    qb = np.clip(qb, 0.0, q_in)
                    return qb


                # --------------------------
                # Standardized LH (Ladson)
                # --------------------------
                def lyne_hollick_ladson(q, alpha=0.925, passes=3, pad_n=30):
                    q = np.asarray(q, dtype=float)
                    qp = _reflect_pad_30(q)
                    dirs = [1 if (k % 2 == 0) else -1 for k in range(passes)]

                    qb_prev = None
                    q_in = qp

                    for k, d in enumerate(dirs):
                        if k == 0:
                            qf0 = q_in[0] if d == 1 else q_in[-1]
                        else:
                            q_in = qb_prev
                            qf0 = qb_prev[-1] if d == -1 else qb_prev[0]

                        qb_prev = _lh_single_pass(q_in=q_in, alpha=alpha, direction=d, qf0=qf0)

                    qb = qb_prev[pad_n:-pad_n]
                    bfi = float(np.sum(qb) / np.sum(q))
                    return qb, bfi


                # --------------------------
                # Alpha sensitivity
                # --------------------------
                def alpha_sensitivity(q, alphas, passes=3):
                    results = []
                    for a in alphas:
                        _, bfi = lyne_hollick_ladson(q=q, alpha=float(a), passes=passes)
                        results.append((float(a), bfi))
                    return results


                # --------------------------
                # Knee selection
                # --------------------------
                def select_alpha_knee(alphas, bfis):
                    x = np.asarray(alphas, dtype=float)
                    y = np.asarray(bfis, dtype=float)

                    p0 = np.array([x[0], y[0]])
                    p1 = np.array([x[-1], y[-1]])
                    v = p1 - p0
                    v_norm = np.linalg.norm(v)

                    dists = []
                    for xi, yi in zip(x, y):
                        p = np.array([xi, yi])
                        dist = np.linalg.norm(np.cross(v, p - p0)) / v_norm
                        dists.append(dist)

                    return int(np.argmax(dists))


                # --------------------------
                # Run + plot
                # --------------------------
                alphas_grid = np.linspace(0.90, 0.99, 100)
                results = alpha_sensitivity(q=bass_river_flow, alphas=alphas_grid)

                alphas = [r[0] for r in results]
                bfis = [r[1] for r in results]

                idx = select_alpha_knee(alphas, bfis)
                alpha_star = alphas[idx]
                bfi_star = bfis[idx]
                # print(f'This is the summer threshold {bfi_star}')


                percentile_list = []
                percent_sum = []
                # print(a)
                for elements in a:
                    if float(elements) > 0:
                        percentile_list.append(elements * bfi_star)
                # print(np.mean(percentile_list))
                

                if time_scale == 'Daily':
                    def frequency_weighted_mean(percentile_list):

                        percentile_list = np.array(percentile_list, dtype=float)

                        unique, counts = np.unique(percentile_list, return_counts=True)

                        freq_dict = dict(zip(unique, counts))

                        weights = np.array([1 / freq_dict[x] for x in percentile_list])

                        return np.sum(percentile_list * weights) / np.sum(weights)

                    percentile_list = np.round(percentile_list, 2)                
                    chosen_threshold = frequency_weighted_mean(percentile_list)
                else:
                    chosen_threshold = np.mean(percentile_list)

                # plt.figure()
                # plt.plot(alphas, bfis)
                # plt.scatter([alpha_star], [bfi_star])

                # plt.annotate(
                #     f"Selected (knee)\nalpha={alpha_star:.3f}\nBFI={bfi_star:.3f}",
                #     xy=(alpha_star, bfi_star),
                #     xytext=(10, 10),
                #     textcoords="offset points"
                # )

                # plt.xlabel("alpha")
                # plt.ylabel("BFI")
                # plt.title("BFI sensitivity to alpha (knee selection)")
                # plt.show()

                # print(f"Knee-selected alpha={alpha_star:.3f}, BFI={bfi_star:.3f}")
                # chosen_quantile *= 2
                
                quantiles = {
                    "Q1 (25th Percentile)": df["flow"].quantile(0.25),
                    "Q2 (Median, 50th Percentile)": df["flow"].quantile(0.50),
                    "Q3 (75th Percentile)": df["flow"].quantile(0.75),
                    "80th Percentile": df["flow"].quantile(0.80),
                    "threshold Percentile": st.session_state.baseflow_amp_factor_SF * flashiness * chosen_threshold,
                    # "threshold Percentile": df["flow"].quantile(0.825),
                    "85th Percentile": df["flow"].quantile(0.85)
                }

                # print('These are the Quantiles')
                # print("Quantiles:")
                # for key, value in quantiles.items():
                #     print(f"{key}: {value:.4f}")

                # Calculate additional statistics
                stats = {
                    "Mean": df["flow"].mean(),
                    "Std": df["flow"].std(),
                    "Min": df["flow"].min(),
                    "Max": df["flow"].max(),
                    "IQR": quantiles["Q3 (75th Percentile)"] - quantiles["Q1 (25th Percentile)"],
                    "Outlier Threshold (Q3 + 1.5*IQR)": quantiles["Q3 (75th Percentile)"] + 1.5 * (quantiles["Q3 (75th Percentile)"] - quantiles["Q1 (25th Percentile)"])
                }
                # print("\nAdditional Statistics:")
                # for key, value in stats.items():
                #     print(f"{key}: {value:.4f}")

                threshold = quantiles["threshold Percentile"]

                # Apply threshold for high/low flow
                # if seasonal_delineation == "A":
                #     threshold = quantiles["threshold Percentile"]
                # else:
                #     threshold = quantiles["90th Percentile"]

                # st.write(quantiles["20th Percentile"])
                if threshold < 0.01 and time_scale == 'Hourly':
                    threshold = 0.01

                if threshold < 0.15 and time_scale == 'Daily':
                    threshold = 0.2
                
                df["flow_type"] = df["flow"].apply(lambda x: "High" if x > threshold else "Low")
                high_count = len(df[df["flow_type"] == "High"])
                low_count = len(df[df["flow_type"] == "Low"])
#                     print(f"\nThreshold: {threshold}")
                # print(f"High flow count (> {threshold}): {high_count}")
                # print(f"Low flow count (≤ {threshold}): {low_count}")

                # Create a figure with subplots
                plt.figure(figsize=(15, 10))

                # 1. Histogram
                plt.subplot(2, 2, 1)
                sns.histplot(df["flow"], bins=20, kde=False)
                plt.axvline(x=quantiles["Q1 (25th Percentile)"], color="green", linestyle="--", label="Q1")
                plt.axvline(x=quantiles["Q2 (Median, 50th Percentile)"], color="blue", linestyle="--", label="Q2 (Median)")
                plt.axvline(x=quantiles["Q3 (75th Percentile)"], color="orange", linestyle="--", label="Q3")
                plt.axvline(x=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("Histogram of Flow Values with Quartiles")
                plt.xlabel("Flow Value")
                plt.ylabel("Frequency")
                plt.legend()

                # 2. Box Plot
                plt.subplot(2, 2, 2)
                sns.boxplot(y=df["flow"])
                plt.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("Box Plot of Flow Values")
                plt.ylabel("Flow Value")
                plt.legend()

                # 3. KDE Plot
                plt.subplot(2, 2, 3)
                sns.kdeplot(df["flow"], fill=True)
                plt.axvline(x=quantiles["Q1 (25th Percentile)"], color="green", linestyle="--", label="Q1")
                plt.axvline(x=quantiles["Q2 (Median, 50th Percentile)"], color="blue", linestyle="--", label="Q2 (Median)")
                plt.axvline(x=quantiles["Q3 (75th Percentile)"], color="orange", linestyle="--", label="Q3")
                plt.axvline(x=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("KDE Plot of Flow Values with Quartiles")
                plt.xlabel("Flow Value")
                plt.ylabel("Density")
                plt.legend()

                # 4. Time Series Plot
                plt.subplot(2, 2, 4)
                plt.plot(df.index, df["flow"], label="Flow Values", marker="o")
                plt.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                high_flow = df[df["flow_type"] == "High"]
                plt.scatter(high_flow.index, high_flow["flow"], color="red", label="High Flow", zorder=5)
                plt.title("Time Series of Flow Values with Threshold")
                plt.xlabel("Index")
                plt.ylabel("Flow Value")
                plt.legend()
                plt.grid(True)

                # Adjust layout and display
                plt.tight_layout()
                plt.show()
                st.pyplot(plt)

                # Display first few rows of the DataFrame
                # print("\nDataFrame with Flow Classification:")
                # print(df.head(10))
                threshold3 = threshold
                summer_threshold = threshold3
            else:
                st.write("No data available for Summer analysis.")
                threshold3 = 0
                summer_threshold = threshold3
                





















            if len(fall) > 0:
                st.header("Fall Analysis")
                data = fall
                
                # Create DataFrame
                df = pd.DataFrame(data, columns=["flow"])

                #Fall Lyne and Hollick filter
                
                a = df["flow"].fillna(0).tolist()

                # a = df["flow"].tolist()
                bass_river_flow = np.array(a)
                # --------------------------
                # Padding
                # --------------------------
                def _reflect_pad_30(q):
                    left = q[1:31][::-1]
                    right = q[-31:-1][::-1]
                    return np.concatenate([left, q, right])


                # --------------------------
                # Single Lyne-Hollick pass
                # --------------------------
                def _lh_single_pass(q_in, alpha, direction, qf0):
                    n = len(q_in)
                    qf = np.empty(n, dtype=float)

                    if direction == 1:
                        qf[0] = qf0
                        for i in range(1, n):
                            qf[i] = alpha * qf[i - 1] + (1 + alpha) / 2.0 * (q_in[i] - q_in[i - 1])
                    else:
                        qf[-1] = qf0
                        for i in range(n - 2, -1, -1):
                            qf[i] = alpha * qf[i + 1] + (1 + alpha) / 2.0 * (q_in[i] - q_in[i + 1])

                    qb = q_in - qf
                    qb = np.clip(qb, 0.0, q_in)
                    return qb


                # --------------------------
                # Standardized LH (Ladson)
                # --------------------------
                def lyne_hollick_ladson(q, alpha=0.925, passes=3, pad_n=30):
                    q = np.asarray(q, dtype=float)
                    qp = _reflect_pad_30(q)
                    dirs = [1 if (k % 2 == 0) else -1 for k in range(passes)]

                    qb_prev = None
                    q_in = qp

                    for k, d in enumerate(dirs):
                        if k == 0:
                            qf0 = q_in[0] if d == 1 else q_in[-1]
                        else:
                            q_in = qb_prev
                            qf0 = qb_prev[-1] if d == -1 else qb_prev[0]

                        qb_prev = _lh_single_pass(q_in=q_in, alpha=alpha, direction=d, qf0=qf0)

                    qb = qb_prev[pad_n:-pad_n]
                    bfi = float(np.sum(qb) / np.sum(q))
                    return qb, bfi


                # --------------------------
                # Alpha sensitivity
                # --------------------------
                def alpha_sensitivity(q, alphas, passes=3):
                    results = []
                    for a in alphas:
                        _, bfi = lyne_hollick_ladson(q=q, alpha=float(a), passes=passes)
                        results.append((float(a), bfi))
                    return results


                # --------------------------
                # Knee selection
                # --------------------------
                def select_alpha_knee(alphas, bfis):
                    x = np.asarray(alphas, dtype=float)
                    y = np.asarray(bfis, dtype=float)

                    p0 = np.array([x[0], y[0]])
                    p1 = np.array([x[-1], y[-1]])
                    v = p1 - p0
                    v_norm = np.linalg.norm(v)

                    dists = []
                    for xi, yi in zip(x, y):
                        p = np.array([xi, yi])
                        dist = np.linalg.norm(np.cross(v, p - p0)) / v_norm
                        dists.append(dist)

                    return int(np.argmax(dists))


                # --------------------------
                # Run + plot
                # --------------------------
                alphas_grid = np.linspace(0.90, 0.99, 100)
                results = alpha_sensitivity(q=bass_river_flow, alphas=alphas_grid)

                alphas = [r[0] for r in results]
                bfis = [r[1] for r in results]

                idx = select_alpha_knee(alphas, bfis)
                alpha_star = alphas[idx]
                bfi_star = bfis[idx]
                # print(f'This is the fall threshold {bfi_star}')


                percentile_list = []
                percent_sum = []
                # print(a)
                for elements in a:
                    if float(elements) > 0:
                        percentile_list.append(elements * bfi_star)
                # print(np.mean(percentile_list))
                

                if time_scale == 'Daily':
                    def frequency_weighted_mean(percentile_list):

                        percentile_list = np.array(percentile_list, dtype=float)

                        unique, counts = np.unique(percentile_list, return_counts=True)

                        freq_dict = dict(zip(unique, counts))

                        weights = np.array([1 / freq_dict[x] for x in percentile_list])

                        return np.sum(percentile_list * weights) / np.sum(weights)

                    percentile_list = np.round(percentile_list, 2)              
                    chosen_threshold = frequency_weighted_mean(percentile_list)
                else:
                    chosen_threshold = np.mean(percentile_list)

                # plt.figure()
                # plt.plot(alphas, bfis)
                # plt.scatter([alpha_star], [bfi_star])

                # plt.annotate(
                #     f"Selected (knee)\nalpha={alpha_star:.3f}\nBFI={bfi_star:.3f}",
                #     xy=(alpha_star, bfi_star),
                #     xytext=(10, 10),
                #     textcoords="offset points"
                # )

                # plt.xlabel("alpha")
                # plt.ylabel("BFI")
                # plt.title("BFI sensitivity to alpha (knee selection)")
                # plt.show()

                # print(f"Knee-selected alpha={alpha_star:.3f}, BFI={bfi_star:.3f}")
                # chosen_quantile *= 2
                
                quantiles = {
                    "Q1 (25th Percentile)": df["flow"].quantile(0.25),
                    "Q2 (Median, 50th Percentile)": df["flow"].quantile(0.50),
                    "Q3 (75th Percentile)": df["flow"].quantile(0.75),
                    "80th Percentile": df["flow"].quantile(0.80),
                    "threshold Percentile": st.session_state.baseflow_amp_factor_SF * flashiness * chosen_threshold,
                    # "threshold Percentile": df["flow"].quantile(0.825),
                    "85th Percentile": df["flow"].quantile(0.85)
                }
                

                # print('These are the Quantiles')
                # print("Quantiles:")
                # for key, value in quantiles.items():
                #     st.write(f"{key}: {value:.4f}")

                # Calculate additional statistics
                stats = {
                    "Mean": df["flow"].mean(),
                    "Std": df["flow"].std(),
                    "Min": df["flow"].min(),
                    "Max": df["flow"].max(),
                    "IQR": quantiles["Q3 (75th Percentile)"] - quantiles["Q1 (25th Percentile)"],
                    "Outlier Threshold (Q3 + 1.5*IQR)": quantiles["Q3 (75th Percentile)"] + 1.5 * (quantiles["Q3 (75th Percentile)"] - quantiles["Q1 (25th Percentile)"])
                }
                # print("\nAdditional Statistics:")
                # for key, value in stats.items():
                #     print(f"{key}: {value:.4f}")

                threshold = quantiles["threshold Percentile"]

                # Apply threshold for high/low flow
                # if seasonal_delineation == "A":
                #         threshold = quantiles["threshold Percentile"]
                # else:
                #     threshold = quantiles["threshold Percentile"]

                if threshold < 0.01 and time_scale == 'Hourly':
                    threshold = 0.01

                if threshold < 0.15 and time_scale == 'Daily':
                    threshold = 0.2


                df["flow_type"] = df["flow"].apply(lambda x: "High" if x > threshold else "Low")
                high_count = len(df[df["flow_type"] == "High"])
                low_count = len(df[df["flow_type"] == "Low"])
#                     print(f"\nThreshold: {threshold}")
                # print(f"High flow count (> {threshold}): {high_count}")
                # print(f"Low flow count (≤ {threshold}): {low_count}")

                # Create a figure with subplots
                plt.figure(figsize=(15, 10))

                # 1. Histogram
                plt.subplot(2, 2, 1)
                sns.histplot(df["flow"], bins=20, kde=False)
                plt.axvline(x=quantiles["Q1 (25th Percentile)"], color="green", linestyle="--", label="Q1")
                plt.axvline(x=quantiles["Q2 (Median, 50th Percentile)"], color="blue", linestyle="--", label="Q2 (Median)")
                plt.axvline(x=quantiles["Q3 (75th Percentile)"], color="orange", linestyle="--", label="Q3")
                plt.axvline(x=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("Histogram of Flow Values with Quartiles")
                plt.xlabel("Flow Value")
                plt.ylabel("Frequency")
                plt.legend()

                # 2. Box Plot
                plt.subplot(2, 2, 2)
                sns.boxplot(y=df["flow"])
                plt.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("Box Plot of Flow Values")
                plt.ylabel("Flow Value")
                plt.legend()

                # 3. KDE Plot
                plt.subplot(2, 2, 3)
                sns.kdeplot(df["flow"], fill=True)
                plt.axvline(x=quantiles["Q1 (25th Percentile)"], color="green", linestyle="--", label="Q1")
                plt.axvline(x=quantiles["Q2 (Median, 50th Percentile)"], color="blue", linestyle="--", label="Q2 (Median)")
                plt.axvline(x=quantiles["Q3 (75th Percentile)"], color="orange", linestyle="--", label="Q3")
                plt.axvline(x=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                plt.title("KDE Plot of Flow Values with Quartiles")
                plt.xlabel("Flow Value")
                plt.ylabel("Density")
                plt.legend()

                # 4. Time Series Plot
                plt.subplot(2, 2, 4)
                plt.plot(df.index, df["flow"], label="Flow Values", marker="o")
                plt.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
                high_flow = df[df["flow_type"] == "High"]
                plt.scatter(high_flow.index, high_flow["flow"], color="red", label="High Flow", zorder=5)
                plt.title("Time Series of Flow Values with Threshold")
                plt.xlabel("Index")
                plt.ylabel("Flow Value")
                plt.legend()
                plt.grid(True)

                # Adjust layout and display
                plt.tight_layout()
                plt.show()
                st.pyplot(plt)

                # Display first few rows of the DataFrame
                # print("\nDataFrame with Flow Classification:")
                # print(df.head(10))
                threshold4 = threshold
                fall_threshold = threshold4
            else:
                st.write("No data available for Fall analysis.")
                threshold4 = 0
                fall_threshold = threshold4
                
            # Define the threshold data
            threshold_data = {
                "Season": ["Winter", "Spring", "Summer", "Fall"],
                "Event Flow Threshold": [threshold1, threshold2, threshold3, threshold4]
            }

            # Create a DataFrame
            df_thresholds = pd.DataFrame(threshold_data)

            # Style the DataFrame for better visuals
            def style_dataframe(df):
                return df.style.set_properties(**{
                    'text-align': 'center',
                    'font-size': '14px',
                    'border-color': '#cccccc',
                    'border-style': 'solid',
                    'border-width': '1px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('font-weight', 'bold'), ('background-color', '#f0f0f0'), ('text-align', 'center')]}
                ])

            # Display the table in Streamlit
            st.subheader("Event Flow Threshold Values")
            st.dataframe(style_dataframe(df_thresholds), use_container_width=True)
            
            
        except Exception as e:
            st.write(f"Analysis error: {str(e)}")
