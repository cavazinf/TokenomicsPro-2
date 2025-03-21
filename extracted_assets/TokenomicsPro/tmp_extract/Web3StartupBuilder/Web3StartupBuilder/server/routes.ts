import type { Express, Request, Response } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { 
  insertUserSchema,
  insertProjectSchema,
  insertTokenSchema,
  insertResourceSchema
} from "@shared/schema";
import { z } from "zod";

export async function registerRoutes(app: Express): Promise<Server> {
  // API routes
  
  // User routes
  app.post("/api/users", async (req, res) => {
    try {
      const validatedData = insertUserSchema.parse(req.body);
      const user = await storage.createUser(validatedData);
      res.status(201).json(user);
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ message: error.errors });
      } else {
        res.status(500).json({ message: "Internal server error" });
      }
    }
  });

  app.get("/api/users/:id", async (req, res) => {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      return res.status(400).json({ message: "Invalid user ID" });
    }
    
    const user = await storage.getUser(id);
    if (!user) {
      return res.status(404).json({ message: "User not found" });
    }
    
    res.json(user);
  });

  // Project routes
  app.get("/api/projects", async (req, res) => {
    const userId = req.query.userId ? parseInt(req.query.userId as string) : undefined;
    
    let projects;
    if (userId && !isNaN(userId)) {
      projects = await storage.getProjectsByUserId(userId);
    } else {
      projects = await storage.getProjects();
    }
    
    res.json(projects);
  });

  app.get("/api/projects/:id", async (req, res) => {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      return res.status(400).json({ message: "Invalid project ID" });
    }
    
    const project = await storage.getProject(id);
    if (!project) {
      return res.status(404).json({ message: "Project not found" });
    }
    
    res.json(project);
  });

  app.post("/api/projects", async (req, res) => {
    try {
      const validatedData = insertProjectSchema.parse(req.body);
      const project = await storage.createProject(validatedData);
      res.status(201).json(project);
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ message: error.errors });
      } else {
        res.status(500).json({ message: "Internal server error" });
      }
    }
  });

  app.put("/api/projects/:id", async (req, res) => {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      return res.status(400).json({ message: "Invalid project ID" });
    }
    
    try {
      const updatedProject = await storage.updateProject(id, req.body);
      if (!updatedProject) {
        return res.status(404).json({ message: "Project not found" });
      }
      
      res.json(updatedProject);
    } catch (error) {
      res.status(500).json({ message: "Internal server error" });
    }
  });

  app.delete("/api/projects/:id", async (req, res) => {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      return res.status(400).json({ message: "Invalid project ID" });
    }
    
    const success = await storage.deleteProject(id);
    if (!success) {
      return res.status(404).json({ message: "Project not found" });
    }
    
    res.status(204).end();
  });

  // Token routes
  app.get("/api/projects/:projectId/token", async (req, res) => {
    const projectId = parseInt(req.params.projectId);
    if (isNaN(projectId)) {
      return res.status(400).json({ message: "Invalid project ID" });
    }
    
    const token = await storage.getTokenByProjectId(projectId);
    if (!token) {
      return res.status(404).json({ message: "Token not found for this project" });
    }
    
    res.json(token);
  });

  app.post("/api/tokens", async (req, res) => {
    try {
      const validatedData = insertTokenSchema.parse(req.body);
      const token = await storage.createToken(validatedData);
      res.status(201).json(token);
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ message: error.errors });
      } else {
        res.status(500).json({ message: "Internal server error" });
      }
    }
  });

  app.put("/api/tokens/:id", async (req, res) => {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      return res.status(400).json({ message: "Invalid token ID" });
    }
    
    try {
      const updatedToken = await storage.updateToken(id, req.body);
      if (!updatedToken) {
        return res.status(404).json({ message: "Token not found" });
      }
      
      res.json(updatedToken);
    } catch (error) {
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Resource routes
  app.get("/api/resources", async (req, res) => {
    const resources = await storage.getResources();
    res.json(resources);
  });

  app.get("/api/resources/:id", async (req, res) => {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      return res.status(400).json({ message: "Invalid resource ID" });
    }
    
    const resource = await storage.getResource(id);
    if (!resource) {
      return res.status(404).json({ message: "Resource not found" });
    }
    
    res.json(resource);
  });

  app.post("/api/resources", async (req, res) => {
    try {
      const validatedData = insertResourceSchema.parse(req.body);
      const resource = await storage.createResource(validatedData);
      res.status(201).json(resource);
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ message: error.errors });
      } else {
        res.status(500).json({ message: "Internal server error" });
      }
    }
  });

  // Create HTTP server
  const httpServer = createServer(app);
  
  return httpServer;
}
