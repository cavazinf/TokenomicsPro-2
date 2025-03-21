import { 
  User, InsertUser, users,
  Project, InsertProject, projects,
  Token, InsertToken, tokens,
  Resource, InsertResource, resources
} from "@shared/schema";

export interface IStorage {
  // User operations
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  // Project operations
  getProjects(): Promise<Project[]>;
  getProjectsByUserId(userId: number): Promise<Project[]>;
  getProject(id: number): Promise<Project | undefined>;
  createProject(project: InsertProject): Promise<Project>;
  updateProject(id: number, project: Partial<Project>): Promise<Project | undefined>;
  deleteProject(id: number): Promise<boolean>;
  
  // Token operations
  getTokenByProjectId(projectId: number): Promise<Token | undefined>;
  createToken(token: InsertToken): Promise<Token>;
  updateToken(id: number, token: Partial<Token>): Promise<Token | undefined>;
  
  // Resource operations
  getResources(): Promise<Resource[]>;
  getResource(id: number): Promise<Resource | undefined>;
  createResource(resource: InsertResource): Promise<Resource>;
}

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private projects: Map<number, Project>;
  private tokens: Map<number, Token>;
  private resources: Map<number, Resource>;
  
  private currentUserId: number = 1;
  private currentProjectId: number = 1;
  private currentTokenId: number = 1;
  private currentResourceId: number = 1;

  constructor() {
    this.users = new Map();
    this.projects = new Map();
    this.tokens = new Map();
    this.resources = new Map();
    
    // Add some default learning resources
    this.seedResources();
  }

  // User operations
  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = this.currentUserId++;
    const now = new Date();
    
    // Generate avatar initials from username or displayName
    const displayName = insertUser.displayName || insertUser.username;
    const avatarInitials = displayName
      .split(' ')
      .map(name => name[0])
      .join('')
      .substring(0, 2)
      .toUpperCase();
    
    const user: User = { 
      ...insertUser, 
      id,
      avatarInitials: avatarInitials || 'UN',
      plan: insertUser.plan || 'free'
    };
    
    this.users.set(id, user);
    return user;
  }

  // Project operations
  async getProjects(): Promise<Project[]> {
    return Array.from(this.projects.values());
  }

  async getProjectsByUserId(userId: number): Promise<Project[]> {
    return Array.from(this.projects.values()).filter(
      (project) => project.userId === userId
    );
  }

  async getProject(id: number): Promise<Project | undefined> {
    return this.projects.get(id);
  }

  async createProject(insertProject: InsertProject): Promise<Project> {
    const id = this.currentProjectId++;
    const now = new Date();
    
    const project: Project = {
      ...insertProject,
      id,
      lastEdited: insertProject.lastEdited || now,
      createdAt: now
    };
    
    this.projects.set(id, project);
    return project;
  }

  async updateProject(id: number, projectUpdate: Partial<Project>): Promise<Project | undefined> {
    const project = this.projects.get(id);
    if (!project) return undefined;
    
    const updatedProject = {
      ...project,
      ...projectUpdate,
      lastEdited: new Date()
    };
    
    this.projects.set(id, updatedProject);
    return updatedProject;
  }

  async deleteProject(id: number): Promise<boolean> {
    return this.projects.delete(id);
  }

  // Token operations
  async getTokenByProjectId(projectId: number): Promise<Token | undefined> {
    return Array.from(this.tokens.values()).find(
      (token) => token.projectId === projectId
    );
  }

  async createToken(insertToken: InsertToken): Promise<Token> {
    const id = this.currentTokenId++;
    const now = new Date();
    
    const token: Token = {
      ...insertToken,
      id,
      createdAt: now
    };
    
    this.tokens.set(id, token);
    return token;
  }

  async updateToken(id: number, tokenUpdate: Partial<Token>): Promise<Token | undefined> {
    const token = this.tokens.get(id);
    if (!token) return undefined;
    
    const updatedToken = {
      ...token,
      ...tokenUpdate
    };
    
    this.tokens.set(id, updatedToken);
    return updatedToken;
  }

  // Resource operations
  async getResources(): Promise<Resource[]> {
    return Array.from(this.resources.values());
  }

  async getResource(id: number): Promise<Resource | undefined> {
    return this.resources.get(id);
  }

  async createResource(insertResource: InsertResource): Promise<Resource> {
    const id = this.currentResourceId++;
    const now = new Date();
    
    const resource: Resource = {
      ...insertResource,
      id,
      createdAt: now
    };
    
    this.resources.set(id, resource);
    return resource;
  }

  // Seed initial data
  private seedResources() {
    const resources: InsertResource[] = [
      {
        title: "Tokenomics 101: Building a Sustainable Model",
        description: "Learn the fundamentals of designing a token economy that creates long-term value.",
        type: "guide",
        imageBackground: "primary-500",
        imageIcon: "polygon",
        link: "/learning-hub/tokenomics-101",
        linkText: "Read Guide",
      },
      {
        title: "Token Vesting Strategies Explained",
        description: "Discover the best approaches to token vesting for different stakeholder groups.",
        type: "tutorial",
        imageBackground: "secondary-500",
        imageIcon: "monitor",
        link: "/learning-hub/vesting-strategies",
        linkText: "Watch Tutorial",
      },
      {
        title: "Economic Models Case Studies",
        description: "Analyze successful token economic models and learn from real-world examples.",
        type: "case_study",
        imageBackground: "green-500",
        imageIcon: "file-text",
        link: "/learning-hub/case-studies",
        linkText: "View Case Studies",
      }
    ];

    resources.forEach(resource => {
      this.createResource(resource);
    });
  }
}

export const storage = new MemStorage();
