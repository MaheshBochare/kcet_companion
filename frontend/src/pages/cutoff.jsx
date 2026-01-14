import DashboardLayout from "../components/cutoff/DashboardLayout";
import CutoffContent from "../components/cutoff/CutoffContent";  // move your current Cutoff logic here

export default function Cutoff() {
  return (
    <DashboardLayout>
      <CutoffContent />
    </DashboardLayout>
  );
}
