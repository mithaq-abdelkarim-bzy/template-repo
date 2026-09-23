const styles = {
    container: {
        display: "flex",
        alignItems: "center",
        gap: 8
    },
    label: {
        fontSize: 14,
        color: "#333"
    },
    outerSwitch: {
        position: "relative",
        display: "inline-block",
        width: 50,
        height: 24
    },
    input: {
        opacity: 0,
        width: 0,
        height: 0
    },
    trackOff: {
        position: "absolute",
        cursor: "pointer",
        inset: 0,
        transition: "150ms cubic-bezier(0.4, 0, 0.2, 1)",
        borderRadius: 34,
        backgroundColor: "#ccc"
    },
    knobOff: {
        position: "absolute",
        height: 16,
        width: 16,
        left: 4,
        bottom: 4,
        backgroundColor: "white",
        transition: "150ms cubic-bezier(0.4, 0, 0.2, 1)",
        borderRadius: "50%"
    },
};

styles.trackOn = { ...styles.trackOff, backgroundColor: "#2196F3" }
styles.knobOn = { ...styles.knobOff, transform: "translateX(26px)" }

export default styles;