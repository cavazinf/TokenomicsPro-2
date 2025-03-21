import { pgTable, text, serial, integer, timestamp, json } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// User model
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
  displayName: text("display_name"),
  avatarInitials: text("avatar_initials"),
  plan: text("plan").default("free").notNull(),
});

export const insertUserSchema = createInsertSchema(users).omit({ 
  id: true 
});

// Project model
export const projects = pgTable("projects", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  status: text("status").notNull().default("draft"), // draft, in_progress, completed
  userId: integer("user_id").notNull(),
  lastEdited: timestamp("last_edited").defaultNow().notNull(),
  tokenDesignProgress: integer("token_design_progress").default(0).notNull(),
  teamMembers: json("team_members").default([]).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertProjectSchema = createInsertSchema(projects).omit({
  id: true,
  createdAt: true,
});

// Token model
export const tokens = pgTable("tokens", {
  id: serial("id").primaryKey(),
  projectId: integer("project_id").notNull(),
  name: text("name").notNull(),
  symbol: text("symbol").notNull(),
  type: text("type").notNull(), // ERC-20, ERC-721, etc.
  totalSupply: text("total_supply").notNull(),
  initialPrice: text("initial_price"),
  initialMarketCap: text("initial_market_cap"),
  circulatingSupply: text("circulating_supply"),
  distribution: json("distribution").default({}).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertTokenSchema = createInsertSchema(tokens).omit({
  id: true,
  createdAt: true,
});

// Resource model (for learning resources)
export const resources = pgTable("resources", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  description: text("description").notNull(),
  type: text("type").notNull(), // guide, tutorial, case_study
  imageBackground: text("image_background").notNull(),
  imageIcon: text("image_icon").notNull(),
  link: text("link").notNull(),
  linkText: text("link_text").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertResourceSchema = createInsertSchema(resources).omit({
  id: true,
  createdAt: true,
});

// Type exports
export type User = typeof users.$inferSelect;
export type InsertUser = z.infer<typeof insertUserSchema>;

export type Project = typeof projects.$inferSelect;
export type InsertProject = z.infer<typeof insertProjectSchema>;

export type Token = typeof tokens.$inferSelect;
export type InsertToken = z.infer<typeof insertTokenSchema>;

export type Resource = typeof resources.$inferSelect;
export type InsertResource = z.infer<typeof insertResourceSchema>;
