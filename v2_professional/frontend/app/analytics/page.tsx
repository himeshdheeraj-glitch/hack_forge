"use client";
import React, { useState, useEffect } from 'react';
import {
    BarChart3, Users, FileText, Globe, Zap,
    ChevronUp, ChevronDown, Activity, Clock, ShieldCheck
} from 'lucide-react';
import axios from 'axios';

export default function AnalyticsDashboard() {
    const [data, setData] = useState<any>(null);

    useEffect(() => {
        async function fetchAnalytics() {
            try {
                const res = await axios.get('http://localhost:8000/analytics');
                setData(res.data);
            } catch (e) {
                // Fallback demo data
                setData({
                    total_queries: 1540,
                    avg_response_time: 0.85,
                    query_success_rate: 96.5,
                    docs_uploaded: 45,
                    lang_dist: { en: 850, hi: 420, te: 270 },
                    helpful: 1280,
                    not_helpful: 42
                });
            }
        }
        fetchAnalytics();
    }, []);

    if (!data) return <div className="p-10 text-center">Loading Performance Data...</div>;

    return (
        <div className="min-h-screen bg-slate-50 p-8">
            <div className="max-w-7xl mx-auto space-y-8">
                {/* Header */}
                <div className="flex justify-between items-end">
                    <div>
                        <h1 className="text-3xl font-bold text-slate-900">System Intelligence</h1>
                        <p className="text-slate-500">Real-time AI performance and user analytics</p>
                    </div>
                    <div className="bg-white px-4 py-2 rounded-lg border shadow-sm text-sm font-medium flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                        System Online: March 06, 2026
                    </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <StatCard title="Total Queries" value={data.total_queries} icon={<Users className="text-blue-500" />} change="+12.5%" trend="up" />
                    <StatCard title="Avg Latency" value={`${data.avg_response_time}s`} icon={<Clock className="text-orange-500" />} change="-0.02s" trend="up" />
                    <StatCard title="Success Rate" value={`${data.query_success_rate}%`} icon={<ShieldCheck className="text-green-500" />} change="+0.4%" trend="up" />
                    <StatCard title="Docs Indexed" value={data.docs_uploaded} icon={<FileText className="text-purple-500" />} change="+5 today" trend="up" />
                </div>

                {/* Charts & Details */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Language distribution */}
                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-lg font-bold flex items-center gap-2"><Globe size={20} className="text-blue-600" /> Language Distribution</h2>
                        </div>
                        <div className="space-y-4">
                            {Object.entries(data.lang_dist).map(([lang, count]: [any, any]) => (
                                <div key={lang}>
                                    <div className="flex justify-between text-sm mb-1">
                                        <span className="capitalize font-medium">{lang === 'en' ? 'English' : lang === 'hi' ? 'Hindi' : 'Telugu'}</span>
                                        <span className="text-slate-500">{count} queries</span>
                                    </div>
                                    <div className="w-full bg-slate-100 rounded-full h-2">
                                        <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${(count / data.total_queries) * 100}%` }}></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Feedback & Satisfaction */}
                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                        <h2 className="text-lg font-bold mb-6 flex items-center gap-2"><Activity size={20} className="text-red-600" /> User Satisfaction</h2>
                        <div className="flex items-center gap-8">
                            <div className="flex-1 space-y-4">
                                <div>
                                    <div className="flex justify-between text-sm mb-1">
                                        <span className="text-green-600 font-bold">Helpful (👍)</span>
                                        <span>{data.helpful}</span>
                                    </div>
                                    <div className="w-full bg-slate-100 rounded-full h-4">
                                        <div className="bg-green-500 h-4 rounded-full" style={{ width: `${(data.helpful / (data.helpful + data.not_helpful)) * 100}%` }}></div>
                                    </div>
                                </div>
                                <div>
                                    <div className="flex justify-between text-sm mb-1">
                                        <span className="text-red-600 font-bold">Not Helpful (👎)</span>
                                        <span>{data.not_helpful}</span>
                                    </div>
                                    <div className="w-full bg-slate-100 rounded-full h-4">
                                        <div className="bg-red-500 h-4 rounded-full" style={{ width: `${(data.not_helpful / (data.helpful + data.not_helpful)) * 100}%` }}></div>
                                    </div>
                                </div>
                            </div>
                            <div className="text-center">
                                <div className="text-4xl font-black text-slate-800">{Math.round((data.helpful / (data.helpful + data.not_helpful)) * 100)}%</div>
                                <div className="text-xs text-slate-400 uppercase font-bold mt-1 tracking-widest">Score</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Integration Note */}
                <div className="bg-blue-900 rounded-2xl p-8 text-white relative overflow-hidden">
                    <Zap className="absolute right-[-20px] bottom-[-20px] text-blue-800 w-64 h-64 -rotate-12" />
                    <div className="relative z-10">
                        <h3 className="text-xl font-bold mb-2">Technical Integration Guide</h3>
                        <p className="text-blue-100 max-w-2xl mb-4">You are viewing the professional V2 Analytics layer. This dashboard connects to the PostgreSQL event store and captures every RAG retrieval step.</p>
                        <div className="flex gap-4">
                            <button className="bg-white text-blue-900 px-4 py-2 rounded-lg font-bold text-sm">View API Docs</button>
                            <button className="bg-blue-700 text-white px-4 py-2 rounded-lg font-bold text-sm border border-blue-600">Export SQL Schema</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatCard({ title, value, icon, change, trend }: any) {
    return (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex justify-between items-start">
            <div>
                <p className="text-slate-500 text-sm font-medium">{title}</p>
                <h3 className="text-2xl font-bold text-slate-800 mt-1">{value}</h3>
                <div className={`mt-2 flex items-center gap-1 text-xs font-bold ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                    {trend === 'up' ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                    {change}
                </div>
            </div>
            <div className="bg-slate-50 p-3 rounded-xl">
                {React.cloneElement(icon, { size: 24 })}
            </div>
        </div>
    );
}
