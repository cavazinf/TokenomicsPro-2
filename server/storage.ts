import { 
  InsertProject, 
  InsertUser, 
  User, 
  Project, 
  TokenModel, 
  InsertTokenModel, 
  DistributionPlan, 
  InsertDistributionPlan, 
  StartupPlan, 
  InsertStartupPlan 
} from "@shared/schema";
import session from "express-session";
import createMemoryStore from "memorystore";

const MemoryStore = createMemoryStore(session);

export interface IStorage {
  // User methods
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  // Project methods
  getProject(id: number): Promise<Project | undefined>;
  getProjectsByUserId(userId: number): Promise<Project[]>;
  createProject(project: InsertProject): Promise<Project>;
  updateProject(id: number, project: Partial<Project>): Promise<Project | undefined>;
  
  // Token model methods
  getTokenModel(id: number): Promise<TokenModel | undefined>;
  getTokenModelsByProjectId(projectId: number): Promise<TokenModel[]>;
  createTokenModel(tokenModel: InsertTokenModel): Promise<TokenModel>;
  
  // Distribution plan methods
  getDistributionPlan(id: number): Promise<DistributionPlan | undefined>;
  getDistributionPlansByProjectId(projectId: number): Promise<DistributionPlan[]>;
  createDistributionPlan(plan: InsertDistributionPlan): Promise<DistributionPlan>;
  
  // Startup plan methods
  getStartupPlan(id: number): Promise<StartupPlan | undefined>;
  getStartupPlansByProjectId(projectId: number): Promise<StartupPlan[]>;
  createStartupPlan(plan: InsertStartupPlan): Promise<StartupPlan>;
  
  // Session store
  sessionStore: session.SessionStore;
}

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private projects: Map<number, Project>;
  private tokenModels: Map<number, TokenModel>;
  private distributionPlans: Map<number, DistributionPlan>;
  private startupPlans: Map<number, StartupPlan>;
  private userIdCounter: number;
  private projectIdCounter: number;
  private tokenModelIdCounter: number;
  private distributionPlanIdCounter: number;
  private startupPlanIdCounter: number;
  sessionStore: session.SessionStore;

  constructor() {
    this.users = new Map();
    this.projects = new Map();
    this.tokenModels = new Map();
    this.distributionPlans = new Map();
    this.startupPlans = new Map();
    this.userIdCounter = 1;
    this.projectIdCounter = 1;
    this.tokenModelIdCounter = 1;
    this.distributionPlanIdCounter = 1;
    this.startupPlanIdCounter = 1;
    this.sessionStore = new MemoryStore({
      checkPeriod: 86400000, // 24 hours
    });
    
    // Add default admin user
    this.createDefaultAdminUser();
  }
  
  private async createDefaultAdminUser() {
    // Check if admin user already exists
    const existingUser = await this.getUserByUsername("admin");
    if (!existingUser) {
      // Create a password hash for "123"
      const passwordHash = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92.3e2dbe29b0a865e64410c02eea523cf0"; // hashed value of "123"
      
      // Add admin user
      const adminUser: User = {
        id: this.userIdCounter++,
        username: "admin",
        password: passwordHash,
        name: "Administrator",
        email: "admin@tokenomicspro.com",
        createdAt: new Date()
      };
      
      this.users.set(adminUser.id, adminUser);
      console.log("Default admin user created with username: 'admin' and password: '123'");
    }
  }

  // User methods
  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username.toLowerCase() === username.toLowerCase(),
    );
  }

  async createUser(userData: InsertUser): Promise<User> {
    const id = this.userIdCounter++;
    const now = new Date();
    const user: User = { 
      ...userData, 
      id,
      createdAt: now
    };
    this.users.set(id, user);
    return user;
  }

  // Project methods
  async getProject(id: number): Promise<Project | undefined> {
    return this.projects.get(id);
  }

  async getProjectsByUserId(userId: number): Promise<Project[]> {
    return Array.from(this.projects.values()).filter(
      (project) => project.userId === userId
    );
  }

  async createProject(projectData: InsertProject): Promise<Project> {
    const id = this.projectIdCounter++;
    const now = new Date();
    const project: Project = {
      ...projectData,
      id,
      createdAt: now,
      updatedAt: now
    };
    this.projects.set(id, project);
    return project;
  }

  async updateProject(id: number, projectData: Partial<Project>): Promise<Project | undefined> {
    const project = await this.getProject(id);
    if (!project) return undefined;
    
    const updatedProject: Project = {
      ...project,
      ...projectData,
      updatedAt: new Date()
    };
    this.projects.set(id, updatedProject);
    return updatedProject;
  }

  // Token model methods
  async getTokenModel(id: number): Promise<TokenModel | undefined> {
    return this.tokenModels.get(id);
  }

  async getTokenModelsByProjectId(projectId: number): Promise<TokenModel[]> {
    return Array.from(this.tokenModels.values()).filter(
      (model) => model.projectId === projectId
    );
  }

  async createTokenModel(tokenModelData: InsertTokenModel): Promise<TokenModel> {
    const id = this.tokenModelIdCounter++;
    const now = new Date();
    const tokenModel: TokenModel = {
      ...tokenModelData,
      id,
      createdAt: now,
      updatedAt: now
    };
    this.tokenModels.set(id, tokenModel);
    return tokenModel;
  }

  // Distribution plan methods
  async getDistributionPlan(id: number): Promise<DistributionPlan | undefined> {
    return this.distributionPlans.get(id);
  }

  async getDistributionPlansByProjectId(projectId: number): Promise<DistributionPlan[]> {
    return Array.from(this.distributionPlans.values()).filter(
      (plan) => plan.projectId === projectId
    );
  }

  async createDistributionPlan(planData: InsertDistributionPlan): Promise<DistributionPlan> {
    const id = this.distributionPlanIdCounter++;
    const now = new Date();
    const plan: DistributionPlan = {
      ...planData,
      id,
      createdAt: now,
      updatedAt: now
    };
    this.distributionPlans.set(id, plan);
    return plan;
  }

  // Startup plan methods
  async getStartupPlan(id: number): Promise<StartupPlan | undefined> {
    return this.startupPlans.get(id);
  }

  async getStartupPlansByProjectId(projectId: number): Promise<StartupPlan[]> {
    return Array.from(this.startupPlans.values()).filter(
      (plan) => plan.projectId === projectId
    );
  }

  async createStartupPlan(planData: InsertStartupPlan): Promise<StartupPlan> {
    const id = this.startupPlanIdCounter++;
    const now = new Date();
    const plan: StartupPlan = {
      ...planData,
      id,
      createdAt: now,
      updatedAt: now
    };
    this.startupPlans.set(id, plan);
    return plan;
  }
}

export const storage = new MemStorage();
