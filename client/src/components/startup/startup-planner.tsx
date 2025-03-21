import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { Check, Clock } from "lucide-react";

type PlannerStep = {
  id: number;
  title: string;
  description: string;
  status: "completed" | "in-progress" | "pending";
};

export default function StartupPlanner() {
  const { toast } = useToast();
  
  const steps: PlannerStep[] = [
    {
      id: 1,
      title: "Project Fundamentals",
      description: "Define your startup's core vision and mission",
      status: "completed",
    },
    {
      id: 2,
      title: "Business Model Canvas",
      description: "Define value proposition, revenue streams, and key resources",
      status: "in-progress",
    },
    {
      id: 3,
      title: "Team Structure",
      description: "Define roles, responsibilities, and needed expertise",
      status: "pending",
    },
    {
      id: 4,
      title: "Funding Strategy",
      description: "Plan for seed, private, and public funding rounds",
      status: "pending",
    },
    {
      id: 5,
      title: "Go-to-Market Strategy",
      description: "Develop marketing, community, and launch plans",
      status: "pending",
    },
  ];

  const handleContinueBuilding = () => {
    toast({
      title: "Progress Saved",
      description: "Your startup plan has been updated.",
    });
  };

  return (
    <Card className="bg-surface border-gray-700">
      <CardHeader className="border-b border-gray-700">
        <CardTitle>Startup Planner</CardTitle>
        <CardDescription className="text-gray-400">Build your Web3 startup from the ground up</CardDescription>
      </CardHeader>
      <CardContent className="p-5 space-y-5">
        {steps.map((step) => (
          <div
            key={step.id}
            className={`bg-background rounded-md p-4 border ${
              step.status === "pending" ? "border-gray-700" : "border-gray-700"
            }`}
          >
            <div className="flex items-start">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 flex-shrink-0 ${
                  step.status === "completed"
                    ? "bg-success"
                    : step.status === "in-progress"
                    ? "bg-warning"
                    : "bg-surface-light"
                }`}
              >
                {step.status === "completed" ? (
                  <Check className="h-4 w-4 text-white" />
                ) : step.status === "in-progress" ? (
                  <Clock className="h-4 w-4 text-white" />
                ) : (
                  <div className={`text-gray-400 font-medium`}>{step.id}</div>
                )}
              </div>
              <div>
                <h3 className={`font-medium ${step.status === "pending" ? "text-gray-400" : ""}`}>{step.title}</h3>
                <p className={`text-sm mt-1 ${step.status === "pending" ? "text-gray-500" : "text-gray-400"}`}>
                  {step.description}
                </p>
              </div>
              <div className="ml-auto">
                <span
                  className={`text-xs px-2 py-0.5 rounded ${
                    step.status === "completed"
                      ? "bg-success/20 text-success"
                      : step.status === "in-progress"
                      ? "bg-warning/20 text-warning"
                      : "bg-surface-light text-gray-400"
                  }`}
                >
                  {step.status === "completed"
                    ? "Completed"
                    : step.status === "in-progress"
                    ? "In Progress"
                    : "Pending"}
                </span>
              </div>
            </div>
          </div>
        ))}

        <Button onClick={handleContinueBuilding} className="w-full bg-primary hover:bg-primary/90">
          Continue Building
        </Button>
      </CardContent>
    </Card>
  );
}
