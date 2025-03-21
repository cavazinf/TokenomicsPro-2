import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { UserPlus, MoreHorizontal } from "lucide-react";

type TeamMember = {
  id: string;
  initials: string;
  name: string;
  role: string;
};

type TeamRole = {
  id: string;
  title: string;
  description: string;
  priority: "high" | "medium" | "low";
};

export default function TeamBuilder() {
  const coreTeam: TeamMember[] = [
    { id: "ac", initials: "AC", name: "Alex Chandler", role: "Project Lead & Tokenomics" },
    { id: "jl", initials: "JL", name: "Jamie Liu", role: "Lead Developer" },
    { id: "mn", initials: "MN", name: "Maria Novak", role: "Marketing & Community" },
  ];

  const advisors: TeamMember[] = [
    { id: "sk", initials: "SK", name: "Sarah Kim", role: "Tokenomics Expert" },
  ];

  const neededRoles: TeamRole[] = [
    {
      id: "security",
      title: "Blockchain Security Expert",
      description: "Smart contract auditing & security",
      priority: "high",
    },
    {
      id: "ui-ux",
      title: "UI/UX Designer",
      description: "Frontend design & user experience",
      priority: "medium",
    },
  ];

  return (
    <Card className="bg-surface border-gray-700">
      <CardHeader className="border-b border-gray-700">
        <CardTitle>Team Builder</CardTitle>
        <CardDescription className="text-gray-400">Organize your project team and roles</CardDescription>
      </CardHeader>
      <CardContent className="p-5">
        <div className="mb-4">
          <div className="flex justify-between mb-3">
            <h3 className="text-sm font-medium">Core Team</h3>
            <button className="text-xs text-primary">Add Member</button>
          </div>

          <div className="space-y-3">
            {coreTeam.map((member) => (
              <div key={member.id} className="bg-background rounded-md p-3 border border-gray-700">
                <div className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-surface-light flex items-center justify-center mr-3">
                    <span className="text-xs">{member.initials}</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-sm">{member.name}</h4>
                    <p className="text-xs text-gray-400">{member.role}</p>
                  </div>
                  <div className="ml-auto text-gray-400">
                    <MoreHorizontal className="h-4 w-4" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="mb-4">
          <div className="flex justify-between mb-3">
            <h3 className="text-sm font-medium">Advisors</h3>
            <button className="text-xs text-primary">Add Advisor</button>
          </div>

          {advisors.map((advisor) => (
            <div key={advisor.id} className="bg-background rounded-md p-3 border border-gray-700">
              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-surface-light flex items-center justify-center mr-3">
                  <span className="text-xs">{advisor.initials}</span>
                </div>
                <div>
                  <h4 className="font-medium text-sm">{advisor.name}</h4>
                  <p className="text-xs text-gray-400">{advisor.role}</p>
                </div>
                <div className="ml-auto text-gray-400">
                  <MoreHorizontal className="h-4 w-4" />
                </div>
              </div>
            </div>
          ))}
        </div>

        <div>
          <div className="flex justify-between mb-3">
            <h3 className="text-sm font-medium">Needed Roles</h3>
            <button className="text-xs text-primary">Add Role</button>
          </div>

          <div className="space-y-3">
            {neededRoles.map((role) => (
              <div key={role.id} className="bg-background rounded-md p-3 border border-gray-700 border-dashed">
                <div className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-surface-light flex items-center justify-center mr-3">
                    <UserPlus className="h-4 w-4 text-gray-400" />
                  </div>
                  <div>
                    <h4 className="font-medium text-sm">{role.title}</h4>
                    <p className="text-xs text-gray-400">{role.description}</p>
                  </div>
                  <div className="ml-auto">
                    <span
                      className={`text-xs px-2 py-0.5 rounded ${
                        role.priority === "high"
                          ? "bg-error/20 text-error"
                          : role.priority === "medium"
                          ? "bg-warning/20 text-warning"
                          : "bg-info/20 text-info"
                      }`}
                    >
                      {role.priority === "high" ? "Priority" : role.priority === "medium" ? "Medium" : "Low"}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
