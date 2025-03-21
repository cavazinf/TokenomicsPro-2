import { Badge } from "@/components/ui/badge";
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { formatDistanceToNow } from "date-fns";

interface TeamMember {
  initials: string;
  name: string;
  color: string;
}

interface ProjectCardProps {
  name: string;
  lastEdited: Date;
  status: "draft" | "in_progress" | "completed";
  progress: number;
  teamMembers: TeamMember[];
  onEdit?: () => void;
  onDelete?: () => void;
  onShare?: () => void;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({
  name,
  lastEdited,
  status,
  progress,
  teamMembers,
  onEdit,
  onDelete,
  onShare,
}) => {
  // Define status badge color
  const statusColorMap = {
    draft: "bg-yellow-100 text-yellow-700",
    in_progress: "bg-blue-100 text-blue-700",
    completed: "bg-green-100 text-green-700",
  };

  // Format status display
  const statusDisplay = {
    draft: "Draft",
    in_progress: "In Progress",
    completed: "Completed",
  };

  // Format last edited date
  const formattedLastEdited = formatDistanceToNow(lastEdited, { addSuffix: true });

  return (
    <div className="bg-card rounded-xl shadow-md hover:shadow-lg transition-shadow p-6 border border-border">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-semibold text-foreground">{name}</h3>
          <p className="text-sm text-muted-foreground">Last edited {formattedLastEdited}</p>
        </div>
        <Badge className={statusColorMap[status]}>
          {statusDisplay[status]}
        </Badge>
      </div>
      
      <div className="mt-4">
        <div className="flex items-center justify-between text-sm mb-1">
          <span className="text-muted-foreground">Token Design</span>
          <span className="font-medium text-foreground">{progress}%</span>
        </div>
        <div className="w-full bg-accent rounded-full h-2">
          <div 
            className={`h-2 rounded-full ${
              status === 'completed' ? 'bg-green-500' : 
              status === 'draft' ? 'bg-yellow-500' : 'bg-primary'
            }`} 
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>
      
      <div className="flex justify-between items-center mt-6">
        <div className="flex -space-x-2">
          {teamMembers.map((member, index) => (
            <div 
              key={index}
              className={`h-7 w-7 rounded-full ${member.color} border-2 border-white flex items-center justify-center text-xs font-medium`}
              title={member.name}
            >
              {member.initials}
            </div>
          ))}
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger className="text-dark-50 hover:text-dark-900">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
              <circle cx="12" cy="12" r="1"></circle>
              <circle cx="19" cy="12" r="1"></circle>
              <circle cx="5" cy="12" r="1"></circle>
            </svg>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={onEdit}>Edit Project</DropdownMenuItem>
            <DropdownMenuItem onClick={onShare}>Share</DropdownMenuItem>
            <DropdownMenuItem 
              onClick={onDelete}
              className="text-red-600 focus:text-red-600"
            >
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  );
};
