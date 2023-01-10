from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import pandas as pd
import numpy as ny
import ast
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.template import context
import csv
from urllib.parse import urlencode
from django.shortcuts import redirect, render
from .forms import SurveyForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

# Create your views here.


def home_page(request):
    return render(request, "home/index.html")


def analytics_page(request):
    return render(request, "home/analytics.html")


def engineering(request):
    query_string = {}
    query_string["course"] = "engineering"
    return render(request, "home/list_all_college.html", query_string)


def design(request):
    query_string = {}
    query_string["course"] = "design"
    return render(request, "home/list_all_college.html", query_string)


def law(request):
    query_string = {}
    query_string["course"] = "law"
    return render(request, "home/list_all_college.html", query_string)


def medical(request):
    query_string = {}
    query_string["course"] = "medical"
    return render(request, "home/list_all_college.html", query_string)


def management(request):
    query_string = {}
    query_string["course"] = "management"
    return render(request, "home/list_all_college.html", query_string)


def science(request):
    query_string = {}
    query_string["course"] = "science"
    return render(request, "home/list_all_college.html", query_string)


def list_all_clgs(request):
    course_name = str(request.GET.get("course"))
    filenames = [
        "static/Final_Dataset/top_clgs_new_btech",
        "static/Final_Dataset/top_clgs_new_bba",
        "static/Final_Dataset/top_clgs_new_mbbs",
        "static/Final_Dataset/top_clgs_new_bdes",
        "static/Final_Dataset/top_clgs_new_llb",
        "static/Final_Dataset/top_clgs_new_bsc",
    ]
    if course_name == "engineering":
        filename = filenames[0]
    elif course_name == "medical":
        filename = filenames[2]
    elif course_name == "management":
        filename = filenames[1]
    elif course_name == "design":
        filename = filenames[3]
    elif course_name == "science":
        filename = filenames[5]
    elif course_name == "law":
        filename = filenames[4]
    with open(filename + ".csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        data = pd.DataFrame(data=rows[1:], columns=rows[0])
        data["Fee Range"] = data["Fee Range"].astype(str)
        data["Duration"] = data["Duration"].astype(str)
        selecting_features = [
            "College Name",
            "College City",
            "State",
            "Exam",
            "Fee Range",
            "Type Of College",
            "Program Type",
            "Duration",
        ]
        for feature in selecting_features:
            data[feature] = data[feature].fillna("")
        Colleges = (
            data["College Name"]
            + data["College City"]
            + data["State"]
            + data["Exam"]
            + data["Fee Range"]
            + data["Type Of College"]
            + data["Program Type"]
            + data["Duration"]
        )
        values = list()
        i = 0
        for ind in range(0, 50):
            list1 = list()
            list1.append(data["College Name"][ind])
            list1.append(data["College City"][ind])
            list1.append(data["State"][ind])
            if len(ast.literal_eval(data["Approvals"][ind])) > 0:
                list1.append(ast.literal_eval(data["Approvals"][ind])[0])
            else:
                list1.append("Not Updated")
            list1.append(data["Rating"][ind])
            list1.append(data["Logo"][ind])
            list1.append(data["Cover"][ind])
            if len(ast.literal_eval(data["Ranking Data"][ind])) > 0:
                list1.append(ast.literal_eval(data["Ranking Data"][ind]))
            else:
                list1.append("Not Updated")
            list1.append(data["Exam"][ind])
            list1.append(data["Facilities"][ind])
            list1.append(data["Fees"][ind])
            list1.append(data["Type Of College"][ind])
            list1.append(data["Program Type"][ind])
            values.append(list1)
            i += 1
            if i >= 15:
                break
    return JsonResponse(values, safe=False)


def similarity(request, params):
    try:
        survey_opt = params
        filenames = [
            "static/Final_Dataset/top_clgs_new_btech",
            "static/Final_Dataset/top_clgs_new_bba",
            "static/Final_Dataset/top_clgs_new_mbbs",
            "static/Final_Dataset/top_clgs_new_bdes",
            "static/Final_Dataset/top_clgs_new_llb",
            "static/Final_Dataset/top_clgs_new_bsc",
        ]
        if survey_opt["course"] == "engineering":
            filename = filenames[0]
        elif survey_opt["course"] == "medical":
            filename = filenames[2]
        elif survey_opt["course"] == "management":
            filename = filenames[1]
        elif survey_opt["course"] == "design":
            filename = filenames[3]
        elif survey_opt["course"] == "science":
            filename = filenames[5]
        elif survey_opt["course"] == "law":
            filename = filenames[4]

        with open(filename + ".csv", "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            data = pd.DataFrame(data=rows[1:], columns=rows[0])
            data["Fee Range"] = data["Fee Range"].astype(str)
            data["Duration"] = data["Duration"].astype(str)
            selecting_features = [
                "College Name",
                "College City",
                "State",
                "Exam",
                "Fee Range",
                "Type Of College",
                "Program Type",
                "Duration",
            ]
            for feature in selecting_features:
                data[feature] = data[feature].fillna("")
            combine_data = (
                data["College Name"]
                + data["College City"]
                + data["State"]
                + data["Exam"]
                + data["Fee Range"]
                + data["Type Of College"]
                + data["Program Type"]
                + data["Duration"]
            )
            vectorizer = TfidfVectorizer()
            feature_vectors = vectorizer.fit_transform(combine_data)
            similarity = cosine_similarity(feature_vectors)
            choice_state = survey_opt["state"]
            choice_city = survey_opt["city"]
            choice_exam = survey_opt["exam_accepted"]
            choice_fee = survey_opt["avg_fee"]
            choice_type = survey_opt["college_type"]
            choice_program = survey_opt["program_type"]
            choice_duration = survey_opt["course_duration"]

            state_name = data["State"].tolist()
            city_name = data["College City"].tolist()
            exam = data["Exam"].tolist()
            college_name = data["College Name"].tolist()
            Fee = data["Fee Range"].tolist()
            Type = data["Type Of College"].tolist()
            Program = data["Program Type"].tolist()
            Duration = data["Duration"].tolist()
            close_match_state = difflib.get_close_matches(choice_state, state_name)[0]
            close_match_city = difflib.get_close_matches(choice_city, city_name)[0]
            close_match_exam = difflib.get_close_matches(choice_exam, exam)[0]
            close_match_fee = difflib.get_close_matches(choice_fee, Fee)[0]
            close_match_type = difflib.get_close_matches(choice_type, Type)[0]
            close_match_program = difflib.get_close_matches(choice_program, Program)[0]
            close_match_duration = difflib.get_close_matches(choice_duration, Duration)[
                0
            ]
            data.rename(columns={"College City": "City"}, inplace=True)
            data.rename(columns={"Fee Range": "Fee"}, inplace=True)
            data.rename(columns={"Type Of College": "Type"}, inplace=True)
            data.rename(columns={"Program Type": "Program"}, inplace=True)

            Colleges = data[data.State == close_match_state][
                data.City == close_match_city
            ][data.Exam == close_match_exam][data.Type == close_match_type][
                data.Program == close_match_program
            ][
                data.Fee == close_match_fee
            ][
                data.Duration == close_match_duration
            ]
            print(type(Colleges))
            return Colleges
    except:
        return []


def results(request):
    survey_opt = dict()
    survey_opt["course"] = str(request.GET.get("course"))
    survey_opt["state"] = str(request.GET.get("state"))
    survey_opt["city"] = str(request.GET.get("city"))
    survey_opt["exam_accepted"] = str(request.GET.get("exam_accepted"))
    survey_opt["avg_fee"] = str(request.GET.get("avg_fee"))
    survey_opt["college_type"] = str(request.GET.get("college_type"))
    survey_opt["program_type"] = str(request.GET.get("program_type"))
    survey_opt["course_duration"] = str(request.GET.get("course_duration"))
    data = similarity("", params=survey_opt)
    values = list()
    check_duplicate=list()
    try:
        for ind in data.index:
            list1 = list()
            if(data["College Name"][ind] in check_duplicate):
                continue
            else:
                check_duplicate.append(data["College Name"][ind])
            list1.append(data["College Name"][ind])
            list1.append(data["City"][ind])
            list1.append(data["State"][ind])
            if len(ast.literal_eval(data["Approvals"][ind])) > 0:
                list1.append(ast.literal_eval(data["Approvals"][ind])[0])
            else:
                list1.append("Not Updated")
            list1.append(data["Rating"][ind])
            list1.append(data["Logo"][ind])
            list1.append(data["Cover"][ind])
            if len(ast.literal_eval(data["Ranking Data"][ind])) > 0:
                list1.append(ast.literal_eval(data["Ranking Data"][ind]))
            else:
                list1.append("Not Updated")
            list1.append(data["Exam"][ind])
            list1.append(data["Facilities"][ind])
            list1.append(data["Fees"][ind])
            list1.append(data["Type"][ind])
            list1.append(data["Program"][ind])
            values.append(list1)
        return JsonResponse(values, safe=False)
    except:
        return JsonResponse([], safe=False)


def results_page(request):
    survey_opt = dict()
    survey_opt["course"] = str(request.GET.get("course"))
    survey_opt["state"] = str(request.GET.get("state"))
    survey_opt["city"] = str(request.GET.get("city"))
    survey_opt["exam_accepted"] = str(request.GET.get("exam_accepted"))
    survey_opt["avg_fee"] = str(request.GET.get("avg_fee"))
    survey_opt["college_type"] = str(request.GET.get("college_type"))
    survey_opt["program_type"] = str(request.GET.get("program_type"))
    survey_opt["course_duration"] = str(request.GET.get("course_duration"))
    return render(request, "home/result.html", survey_opt)


# Create your views here.


def survey(request):
    if request.method == "POST":
        course = request.POST["course"]
        course_duration = request.POST["course_duration"]
        program_type = request.POST["program_type"]
        college_type = request.POST["college_type"]
        avg_fee = request.POST["avg_fee"]
        exam_accepted = request.POST["exam_accepted"]
        state = request.POST["state"]
        city = request.POST["city"]
        survey_opt = {
            "course": course,
            "course_duration": course_duration,
            "program_type": program_type,
            "college_type": college_type,
            "avg_fee": avg_fee,
            "exam_accepted": exam_accepted,
            "state": state,
            "city": city,
        }
        if len(survey_opt) != 0:
            query_string = urlencode(survey_opt)
            return redirect("/results_page/?" + query_string)
    context = {}
    return render(request, "home/survey.html", context)
