import { pgTable, text, serial, integer, boolean, timestamp, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// User schema
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
  name: text("name"),
  email: text("email"),
  createdAt: timestamp("created_at").defaultNow(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
  name: true,
  email: true,
});

// Project schema
export const projects = pgTable("projects", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  description: text("description"),
  status: text("status").default("active"),
  userId: integer("user_id").references(() => users.id),
  type: text("type").default("tokenomics"), // tokenomics or startup
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export const insertProjectSchema = createInsertSchema(projects).pick({
  name: true,
  description: true,
  status: true,
  userId: true,
  type: true,
});

// Token Model schema
export const tokenModels = pgTable("token_models", {
  id: serial("id").primaryKey(),
  projectId: integer("project_id").references(() => projects.id),
  name: text("name").notNull(),
  tokenType: text("token_type").default("utility"),
  supplyModel: text("supply_model").default("fixed"),
  initialSupply: text("initial_supply").default("100000000"),
  tokenStandard: text("token_standard").default("ERC-20"),
  configuration: jsonb("configuration"),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export const insertTokenModelSchema = createInsertSchema(tokenModels).pick({
  projectId: true,
  name: true,
  tokenType: true,
  supplyModel: true,
  initialSupply: true,
  tokenStandard: true,
  configuration: true,
});

// Distribution Plan schema
export const distributionPlans = pgTable("distribution_plans", {
  id: serial("id").primaryKey(),
  projectId: integer("project_id").references(() => projects.id),
  tokenModelId: integer("token_model_id").references(() => tokenModels.id),
  name: text("name").notNull(),
  distribution: jsonb("distribution"),
  vestingSchedules: jsonb("vesting_schedules"),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export const insertDistributionPlanSchema = createInsertSchema(distributionPlans).pick({
  projectId: true,
  tokenModelId: true,
  name: true,
  distribution: true,
  vestingSchedules: true,
});

// Startup Plan schema
export const startupPlans = pgTable("startup_plans", {
  id: serial("id").primaryKey(),
  projectId: integer("project_id").references(() => projects.id),
  name: text("name").notNull(),
  businessModel: text("business_model"),
  roadmap: jsonb("roadmap"),
  team: jsonb("team"),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export const insertStartupPlanSchema = createInsertSchema(startupPlans).pick({
  projectId: true,
  name: true,
  businessModel: true,
  roadmap: true,
  team: true,
});

// Type definitions
export type User = typeof users.$inferSelect;
export type InsertUser = z.infer<typeof insertUserSchema>;

export type Project = typeof projects.$inferSelect;
export type InsertProject = z.infer<typeof insertProjectSchema>;

export type TokenModel = typeof tokenModels.$inferSelect;
export type InsertTokenModel = z.infer<typeof insertTokenModelSchema>;

export type DistributionPlan = typeof distributionPlans.$inferSelect;
export type InsertDistributionPlan = z.infer<typeof insertDistributionPlanSchema>;

export type StartupPlan = typeof startupPlans.$inferSelect;
export type InsertStartupPlan = z.infer<typeof insertStartupPlanSchema>;
