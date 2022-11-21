#!/bin/sh -e

uvicorn app.main:api ${@}
