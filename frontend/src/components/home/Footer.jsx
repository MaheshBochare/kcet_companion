export default function HomeFooter() {
  return (
    <footer className="footer">
      <p style={{ margin: 0, fontWeight: 500 }}>
        © {new Date().getFullYear()} KCET Admission Companion
      </p>

      <p style={{ margin: "6px 0 0", fontSize: "0.9rem", opacity: 0.9 }}>
        Built with to help students choose the right college
      </p>
    </footer>
  );
}
