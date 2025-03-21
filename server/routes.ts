import type { Express, Request, Response } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { setupAuth } from "./auth";
import { insertProjectSchema, insertTokenModelSchema, insertDistributionPlanSchema, insertStartupPlanSchema } from "@shared/schema";
import { ZodError } from "zod";

export async function registerRoutes(app: Express): Promise<Server> {
  // Sets up authentication routes
  setupAuth(app);

  // Projects API
  app.get("/api/projects", async (req: Request, res: Response) => {
    if (!req.isAuthenticated()) return res.sendStatus(401);
    try {
      const projects = await storage.getProjectsByUserId(req.user!.id);
      res.json(projects);
    } catch (error) {
      res.status(500).json({ error: (error as Error).message });
    }
  });

  app.post("/api/projects", async (req: Request, res: Response) => {
    if (!req.isAuthenticated()) return res.sendStatus(401);
    try {
      const projectData = insertProjectSchema.parse({
        ...req.body,
        userId: req.user!.id
      });
      const project = await storage.createProject(projectData);
      res.status(201).json(project);
    } catch (error) {
      if (error instanceof ZodError) {
        res.status(400).json({ error: error.errors });
      } else {
        res.status(500).json({ error: (error as Error).message });
      }
    }
  });

  app.get("/api/projects/:id", async (req: Request, res: Response) => {
    if (!req.isAuthenticated()) return res.sendStatus(401);
    try {
      const project = await storage.getProject(parseInt(req.params.id));
      if (!project || project.userId !== req.user!.id) {
        return res.status(404).json({ error: "Project not found" });
      }
      res.json(project);
    } catch (error) {
      res.status(500).json({ error: (error as Error).message });
    }
  });

  // Token Models API
  app.get("/api/projects/:projectId/token-models", async (req: Request, res: Response) => {
    if (!req.isAuthenticated()) return res.sendStatus(401);
    try {
      const projectId = parseInt(req.params.projectId);
      const project = await storage.getProject(projectId);
      if (!project || project.userId !== req.user!.id) {
        return res.status(404).json({ error: "Project not found" });
      }
      const tokenModels = await storage.getTokenModelsByProjectId(projectId);
      res.json(tokenModels);
    } catch (error) {
      res.status(500).json({ error: (error as Error).message });
    }
  });

  app.post("/api/token-models", async (req: Request, res: Response) => {
    if (!req.isAuthenticated()) return res.sendStatus(401);
    try {
      const tokenModelData = insertTokenModelSchema.parse(req.body);
      const project = await storage.getProject(tokenModelData.projectId);
      if (!project || project.userId !== req.user!.id) {
        return res.status(404).json({ error: "Project not found" });
      }
      const tokenModel = await storage.createTokenModel(tokenModelData);
      res.status(201).json(tokenModel);
    } catch (error) {
      if (error instanceof ZodError) {
        res.status(400).json({ error: error.errors });
      } else {
        res.status(500).json({ error: (error as Error).message });
      }
    }
  });

  // Distribution Plans API
  app.post("/api/distribution-plans", async (req: Request, res: Response) => {
    if (!req.isAuthenticated()) return res.sendStatus(401);
    try {
      const planData = insertDistributionPlanSchema.parse(req.body);
      const project = await storage.getProject(planData.projectId);
      if (!project || project.userId !== req.user!.id) {
        return res.status(404).json({ error: "Project not found" });
      }
      const plan = await storage.createDistributionPlan(planData);
      res.status(201).json(plan);
    } catch (error) {
      if (error instanceof ZodError) {
        res.status(400).json({ error: error.errors });
      } else {
        res.status(500).json({ error: (error as Error).message });
      }
    }
  });

  // Startup Plans API
  app.post("/api/startup-plans", async (req: Request, res: Response) => {
    if (!req.isAuthenticated()) return res.sendStatus(401);
    try {
      const planData = insertStartupPlanSchema.parse(req.body);
      const project = await storage.getProject(planData.projectId);
      if (!project || project.userId !== req.user!.id) {
        return res.status(404).json({ error: "Project not found" });
      }
      const plan = await storage.createStartupPlan(planData);
      res.status(201).json(plan);
    } catch (error) {
      if (error instanceof ZodError) {
        res.status(400).json({ error: error.errors });
      } else {
        res.status(500).json({ error: (error as Error).message });
      }
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
