"""
Buyers CRUD routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from bson import ObjectId
from ..extensions import mongo
from ..utils.helpers import utcnow, Pagination, build_sort

buyers_bp = Blueprint("buyers", __name__)
COLLECTION = "buyers"


def _get_col():
    return mongo.db[COLLECTION]


# ── List ─────────────────────────────────────────────────────────────────────

@buyers_bp.route("/")
def index():
    col = _get_col()
    page = max(1, request.args.get("page", 1, type=int))
    per_page = current_app.config["ITEMS_PER_PAGE"]
    search = request.args.get("q", "").strip()
    sort_param = request.args.get("sort", "-created_at")

    query = {}
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"location": {"$regex": search, "$options": "i"}},
            {"contact": {"$regex": search, "$options": "i"}},
        ]

    sort_field, sort_dir = build_sort(sort_param)
    total = col.count_documents(query)
    docs = list(
        col.find(query)
        .sort(sort_field, sort_dir)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )

    pagination = Pagination(total, page, per_page)
    return render_template(
        "buyers/index.html",
        buyers=docs,
        pagination=pagination,
        search=search,
        sort=sort_param,
        total=total,
    )


# ── Create ───────────────────────────────────────────────────────────────────

@buyers_bp.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        contact = request.form.get("contact", "").strip()
        location = request.form.get("location", "").strip()

        errors = []
        if not name:
            errors.append("Buyer name is required.")
        if not contact:
            errors.append("Contact details are required.")
        if not location:
            errors.append("Location is required.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("buyers/form.html", action="new", data=request.form)

        _get_col().insert_one({
            "name": name,
            "contact": contact,
            "location": location,
            "created_at": utcnow(),
        })
        flash(f"Buyer '{name}' added successfully.", "success")
        return redirect(url_for("buyers.index"))

    return render_template("buyers/form.html", action="new", data={})


# ── View ─────────────────────────────────────────────────────────────────────

@buyers_bp.route("/<id>")
def view(id):
    doc = _get_col().find_one_or_404({"_id": ObjectId(id)})
    # Linked transactions
    linked = list(mongo.db.records.find({"buyer_id": ObjectId(id)}).sort("date", -1).limit(10))
    return render_template("buyers/view.html", buyer=doc, linked_records=linked)


# ── Edit ─────────────────────────────────────────────────────────────────────

@buyers_bp.route("/<id>/edit", methods=["GET", "POST"])
def edit(id):
    col = _get_col()
    doc = col.find_one_or_404({"_id": ObjectId(id)})

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        contact = request.form.get("contact", "").strip()
        location = request.form.get("location", "").strip()

        errors = []
        if not name:
            errors.append("Buyer name is required.")
        if not contact:
            errors.append("Contact details are required.")
        if not location:
            errors.append("Location is required.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("buyers/form.html", action="edit", data=request.form, doc=doc)

        col.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": name, "contact": contact, "location": location}},
        )
        flash(f"Buyer '{name}' updated.", "success")
        return redirect(url_for("buyers.view", id=id))

    return render_template("buyers/form.html", action="edit", data=doc, doc=doc)


# ── Delete ───────────────────────────────────────────────────────────────────

@buyers_bp.route("/<id>/delete", methods=["POST"])
def delete(id):
    doc = _get_col().find_one_or_404({"_id": ObjectId(id)})
    _get_col().delete_one({"_id": ObjectId(id)})
    flash(f"Buyer '{doc['name']}' deleted.", "warning")
    return redirect(url_for("buyers.index"))
