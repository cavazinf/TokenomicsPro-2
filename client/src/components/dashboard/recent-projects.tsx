import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Folder, Gamepad, ImageIcon } from "lucide-react";
import { Link } from "wouter";

type Project = {
  id: string;
  name: string;
  icon: React.ReactNode;
  iconColor: string;
  iconBgColor: string;
  status: "active" | "completed" | "in-progress";
  lastUpdate: string;
  collaborators: { initials: string }[];
};

export default function RecentProjects() {
  const projects: Project[] = [
    {
      id: "1",
      name: "DeFi Lending Protocol",
      icon: <Folder />,
      iconColor: "text-primary",
      iconBgColor: "bg-primary/20",
      status: "active",
      lastUpdate: "Updated 2 days ago",
      collaborators: [{ initials: "AC" }, { initials: "JL" }],
    },
    {
      id: "2",
      name: "NFT Marketplace",
      icon: <ImageIcon />,
      iconColor: "text-secondary",
      iconBgColor: "bg-secondary/20",
      status: "completed",
      lastUpdate: "Updated 1 week ago",
      collaborators: [{ initials: "AC" }],
    },
    {
      id: "3",
      name: "GameFi Platform",
      icon: <Gamepad />,
      iconColor: "text-accent",
      iconBgColor: "bg-accent/20",
      status: "in-progress",
      lastUpdate: "Updated 3 days ago",
      collaborators: [{ initials: "AC" }, { initials: "MN" }, { initials: "+2" }],
    },
  ];

  return (
    <Card className="bg-surface rounded-lg border border-gray-700">
      <CardHeader className="p-5 border-b border-gray-700">
        <CardTitle>Recent Projects</CardTitle>
      </CardHeader>
      <CardContent className="p-5 space-y-4">
        {projects.map((project) => (
          <div key={project.id} className="flex items-start border-b border-gray-700 pb-4 last:border-0 last:pb-0">
            <div className={`h-10 w-10 rounded ${project.iconBgColor} flex items-center justify-center mr-3 flex-shrink-0`}>
              <div className={project.iconColor}>{project.icon}</div>
            </div>
            <div className="flex-1">
              <div className="flex justify-between">
                <h3 className="font-medium">{project.name}</h3>
                <span
                  className={`text-xs px-2 py-0.5 rounded ${
                    project.status === "active"
                      ? "bg-primary/20 text-primary"
                      : project.status === "completed"
                      ? "bg-success/20 text-success"
                      : "bg-warning/20 text-warning"
                  }`}
                >
                  {project.status === "active" ? "Active" : project.status === "completed" ? "Completed" : "In Progress"}
                </span>
              </div>
              <p className="text-sm text-gray-400 mt-1">{project.lastUpdate}</p>
              <div className="flex items-center mt-2">
                <div className="flex -space-x-2">
                  {project.collaborators.map((collaborator, index) => (
                    <div
                      key={index}
                      className="h-6 w-6 rounded-full bg-surface-light flex items-center justify-center text-xs"
                    >
                      {collaborator.initials}
                    </div>
                  ))}
                </div>
                <span className="text-xs text-gray-400 ml-2">{project.collaborators.length} collaborators</span>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
      <div className="border-t border-gray-700 p-3 text-center">
        <Link href="/projects" className="text-sm text-primary hover:text-primary/90">
          View all projects
        </Link>
      </div>
    </Card>
  );
}
