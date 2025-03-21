import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { Check, Clock, Calendar } from "lucide-react";

type Milestone = {
  id: string;
  title: string;
  timeframe: string;
  status: "completed" | "in-progress" | "planned";
  tasks: string[];
};

export default function RoadmapBuilder() {
  const { toast } = useToast();
  
  const [milestones, setMilestones] = useState<Milestone[]>([
    {
      id: "q4-2023",
      title: "Q4 2023 - Project Inception",
      timeframe: "Q4 2023",
      status: "completed",
      tasks: ["Team formation", "Initial project planning", "Market research & whitepaper"],
    },
    {
      id: "q1-2024",
      title: "Q1 2024 - MVP Development",
      timeframe: "Q1 2024",
      status: "in-progress",
      tasks: [
        "Core protocol development",
        "Basic UI/UX implementation",
        "Token economic model finalization",
        "Initial security audit",
      ],
    },
    {
      id: "q2-2024",
      title: "Q2 2024 - Testnet & Community",
      timeframe: "Q2 2024",
      status: "planned",
      tasks: [
        "Testnet launch",
        "Community building",
        "Private funding round",
        "Partnership announcements",
      ],
    },
    {
      id: "q3-2024",
      title: "Q3 2024 - Mainnet Launch",
      timeframe: "Q3 2024",
      status: "planned",
      tasks: [
        "Mainnet deployment",
        "Token Generation Event",
        "DEX/CEX listings",
        "Marketing campaign",
      ],
    },
  ]);

  const handleAddMilestone = () => {
    toast({
      title: "Add Milestone",
      description: "Creating a new milestone in your roadmap.",
    });
  };

  const handleExportPlan = () => {
    toast({
      title: "Export Complete",
      description: "Your roadmap has been exported successfully.",
    });
  };

  return (
    <Card className="bg-surface border-gray-700">
      <CardHeader className="border-b border-gray-700">
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>Project Roadmap</CardTitle>
            <CardDescription className="text-gray-400">Timeline and milestones for your Web3 project</CardDescription>
          </div>
          <Button variant="outline" size="sm" className="bg-surface-light text-white border-gray-700">
            Edit
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-5">
        <div className="relative">
          <div className="absolute top-0 bottom-0 left-4 w-0.5 bg-gray-700"></div>

          {milestones.map((milestone, index) => (
            <div key={milestone.id} className="relative mb-8">
              <div className="flex items-start">
                <div
                  className={`flex items-center justify-center w-8 h-8 rounded-full flex-shrink-0 z-10 ${
                    milestone.status === "completed"
                      ? "bg-success"
                      : milestone.status === "in-progress"
                      ? "bg-warning"
                      : "bg-surface-light"
                  }`}
                >
                  {milestone.status === "completed" ? (
                    <Check className="h-4 w-4 text-white" />
                  ) : milestone.status === "in-progress" ? (
                    <Clock className="h-4 w-4 text-white" />
                  ) : (
                    <Calendar className="h-4 w-4 text-gray-400" />
                  )}
                </div>
                <div className="flex-1 ml-4">
                  <div className="bg-background p-3 rounded-lg border border-gray-700">
                    <div className="flex flex-wrap justify-between mb-1">
                      <h3 className={`font-medium ${milestone.status === "planned" ? "text-gray-400" : ""}`}>
                        {milestone.title}
                      </h3>
                      <span
                        className={`text-xs px-2 py-0.5 rounded ${
                          milestone.status === "completed"
                            ? "bg-success/20 text-success"
                            : milestone.status === "in-progress"
                            ? "bg-warning/20 text-warning"
                            : "bg-surface-light text-gray-400"
                        }`}
                      >
                        {milestone.status === "completed"
                          ? "Completed"
                          : milestone.status === "in-progress"
                          ? "In Progress"
                          : "Planned"}
                      </span>
                    </div>
                    <ul
                      className={`text-sm space-y-1 list-disc pl-4 ${
                        milestone.status === "planned" ? "text-gray-500" : "text-gray-400"
                      }`}
                    >
                      {milestone.tasks.map((task, taskIndex) => (
                        <li key={taskIndex}>{task}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="flex space-x-2 mt-6">
          <Button onClick={handleAddMilestone} className="flex-1 bg-secondary hover:bg-secondary/90">
            Add Milestone
          </Button>
          <Button onClick={handleExportPlan} variant="outline" className="flex-1 bg-surface-light text-white border-gray-700">
            Export Plan
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
