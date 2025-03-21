import React from 'react';
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { formatDistanceToNow } from 'date-fns';
import { MoreHorizontal, Edit, Trash, Share2 } from 'lucide-react';
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

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
  onEdit = () => {},
  onDelete = () => {},
  onShare = () => {},
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "draft":
        return "text-gray-500";
      case "in_progress":
        return "text-yellow-500";
      case "completed":
        return "text-green-500";
      default:
        return "text-gray-500";
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case "draft":
        return "Draft";
      case "in_progress":
        return "In Progress";
      case "completed":
        return "Completed";
      default:
        return "Unknown";
    }
  };

  return (
    <Card className="p-4 bg-surface-card border border-surface-border hover:border-surface-border-hover">
      <div className="flex justify-between">
        <div>
          <h3 className="font-semibold">{name}</h3>
          <div className="text-sm text-gray-400 mb-2">
            Last edited {formatDistanceToNow(lastEdited, { addSuffix: true })}
          </div>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon">
              <MoreHorizontal className="h-4 w-4" />
              <span className="sr-only">More</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={onEdit}>
              <Edit className="mr-2 h-4 w-4" />
              <span>Edit</span>
            </DropdownMenuItem>
            <DropdownMenuItem onClick={onShare}>
              <Share2 className="mr-2 h-4 w-4" />
              <span>Share</span>
            </DropdownMenuItem>
            <DropdownMenuItem className="text-red-500" onClick={onDelete}>
              <Trash className="mr-2 h-4 w-4" />
              <span>Delete</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <div className="mt-4 mb-2">
        <div className="flex justify-between mb-1">
          <span className="text-xs">Progress</span>
          <span className="text-xs">{progress}%</span>
        </div>
        <Progress value={progress} className="h-1" />
      </div>

      <div className="flex items-center justify-between mt-4">
        <div className="flex -space-x-2">
          {teamMembers.map((member, index) => (
            <div
              key={index}
              className={`w-6 h-6 rounded-full flex items-center justify-center text-xs text-white ${member.color}`}
              title={member.name}
            >
              {member.initials}
            </div>
          ))}
        </div>
        <span className={`text-xs font-medium ${getStatusColor(status)}`}>
          {getStatusText(status)}
        </span>
      </div>
    </Card>
  );
};