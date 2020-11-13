import asyncio
import pytest
import random
import textwrap
from redbot.core.utils import (
    bounded_gather,
    bounded_gather_iter,
    chat_formatting,
    common_filters,
    deduplicate_iterables,
)
from discord import Embed


def test_bordered_symmetrical():
    expected = textwrap.dedent(
        """\
    ┌──────────────┐    ┌─────────────┐
    │one           │    │four         │
    │two           │    │five         │
    │three         │    │six          │
    └──────────────┘    └─────────────┘"""
    )
    col1, col2 = ["one", "two", "three"], ["four", "five", "six"]
    assert chat_formatting.bordered(col1, col2) == expected


def test_bordered_asymmetrical():
    expected = textwrap.dedent(
        """\
    ┌──────────────┐    ┌──────────────┐
    │one           │    │four          │
    │two           │    │five          │
    │three         │    │six           │
    └──────────────┘    │seven         │
                        └──────────────┘"""
    )
    col1, col2 = ["one", "two", "three"], ["four", "five", "six", "seven"]
    assert chat_formatting.bordered(col1, col2) == expected


def test_bordered_asymmetrical_2():
    expected = textwrap.dedent(
        """\
    ┌──────────────┐    ┌─────────────┐
    │one           │    │five         │
    │two           │    │six          │
    │three         │    └─────────────┘
    │four          │                   
    └──────────────┘                   """
    )
    col1, col2 = ["one", "two", "three", "four"], ["five", "six"]
    assert chat_formatting.bordered(col1, col2) == expected


def test_bordered_ascii():
    expected = textwrap.dedent(
        """\
    +--------------+    +-------------+
    |one           |    |four         |
    |two           |    |five         |
    |three         |    |six          |
    +--------------+    +-------------+"""
    )
    col1, col2 = ["one", "two", "three"], ["four", "five", "six"]
    assert chat_formatting.bordered(col1, col2, ascii_border=True) == expected


def test_deduplicate_iterables():
    expected = [1, 2, 3, 4, 5]
    inputs = [[1, 2, 1], [3, 1, 2, 4], [5, 1, 2]]
    assert deduplicate_iterables(*inputs) == expected


@pytest.mark.asyncio
async def test_bounded_gather():
    status = [0, 0]  # num_running, max_running

    async def wait_task(i, delay, status, fail=False):
        status[0] += 1
        await asyncio.sleep(delay)
        status[1] = max(status)
        status[0] -= 1

        if fail:
            raise RuntimeError

        return i

    num_concurrent = random.randint(2, 8)
    num_tasks = random.randint(4 * num_concurrent, 5 * num_concurrent)
    num_fail = random.randint(num_concurrent, num_tasks)

    tasks = [wait_task(i, random.random() / 1000, status) for i in range(num_tasks)]
    tasks += [wait_task(i, random.random() / 1000, status, fail=True) for i in range(num_fail)]

    num_failed = 0

    results = await bounded_gather(*tasks, limit=num_concurrent, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, RuntimeError):
            num_failed += 1
        else:
            assert result == i  # verify_permissions original orde
            assert 0 <= result < num_tasks

    assert 0 < status[1] <= num_concurrent
    assert num_fail == num_failed


@pytest.mark.asyncio
async def test_bounded_gather_iter():
    status = [0, 0]  # num_running, max_running

    async def wait_task(i, delay, status, fail=False):
        status[0] += 1
        await asyncio.sleep(delay)
        status[1] = max(status)
        status[0] -= 1

        if fail:
            raise RuntimeError

        return i

    num_concurrent = random.randint(2, 8)
    num_tasks = random.randint(4 * num_concurrent, 16 * num_concurrent)
    num_fail = random.randint(num_concurrent, num_tasks)

    tasks = [wait_task(i, random.random() / 1000, status) for i in range(num_tasks)]
    tasks += [wait_task(i, random.random() / 1000, status, fail=True) for i in range(num_fail)]
    random.shuffle(tasks)

    num_failed = 0

    for result in bounded_gather_iter(*tasks, limit=num_concurrent):
        try:
            result = await result
        except RuntimeError:
            num_failed += 1
            continue

        assert 0 <= result < num_tasks

    assert 0 < status[1] <= num_concurrent
    assert num_fail == num_failed


@pytest.mark.skip(reason="spams logs with pending task warnings")
@pytest.mark.asyncio
async def test_bounded_gather_iter_cancel():
    status = [0, 0, 0]  # num_running, max_running, num_ran

    async def wait_task(i, delay, status, fail=False):
        status[0] += 1
        await asyncio.sleep(delay)
        status[1] = max(status[:2])
        status[0] -= 1

        if fail:
            raise RuntimeError

        status[2] += 1
        return i

    num_concurrent = random.randint(2, 8)
    num_tasks = random.randint(4 * num_concurrent, 16 * num_concurrent)
    quit_on = random.randint(0, num_tasks)
    num_fail = random.randint(num_concurrent, num_tasks)

    tasks = [wait_task(i, random.random() / 1000, status) for i in range(num_tasks)]
    tasks += [wait_task(i, random.random() / 1000, status, fail=True) for i in range(num_fail)]
    random.shuffle(tasks)

    num_failed = 0
    i = 0

    for result in bounded_gather_iter(*tasks, limit=num_concurrent):
        try:
            result = await result
        except RuntimeError:
            num_failed += 1
            continue

        if i == quit_on:
            break

        assert 0 <= result < num_tasks
        i += 1

    assert 0 < status[1] <= num_concurrent
    assert quit_on <= status[2] <= quit_on + num_concurrent
    assert num_failed <= num_fail


def test_normalize_smartquotes():
    assert common_filters.normalize_smartquotes("Should\u2018 normalize") == "Should' normalize"
    assert common_filters.normalize_smartquotes("Same String") == "Same String"


def test_embed_list():
    base_embed = Embed(title="Test")
    rows = list(str(i) for i in range(11))

    embed_list = chat_formatting.rows_to_embeds(
        rows, base_embed, embed_max_fields=2, field_max_rows=5, greedy_fill=False
    )
    expected_embed_count = 2
    assert expected_embed_count == len(embed_list)
    # Expected field structure: [0 1 2, 3 4 5], [6 7 8, 9 10].
    expected = ((["0", "1", "2"], ["3", "4", "5"]), (["6", "7", "8"], ["9", "10"]))
    for i, e in enumerate(embed_list):
        for j, field in enumerate(getattr(e, "_fields", [])):
            f_expected = "\n".join(expected[i][j])
            f_actual = field["value"]
            assert f_expected == f_actual
        footer = getattr(e, "_footer", {})
        assert footer["text"] == "{} of {}".format(i + 1, expected_embed_count)


def test_embed_list_2():
    base_embed = Embed(title="Test")
    rows = list(str(i) for i in range(11))

    embed_list = chat_formatting.rows_to_embeds(
        rows, base_embed, embed_max_fields=2, field_max_rows=5, greedy_fill=True
    )
    expected_embed_count = 2
    assert expected_embed_count == len(embed_list)
    # Expected field structure: [0 1 2 3 4, 5 6 7 8 9], [10,].
    expected = ((["0", "1", "2", "3", "4"], ["5", "6", "7", "8", "9"]), (["10"],))
    for i, e in enumerate(embed_list):
        for j, field in enumerate(getattr(e, "_fields", [])):
            f_expected = "\n".join(expected[i][j])
            f_actual = field["value"]
            assert f_expected == f_actual
        footer = getattr(e, "_footer", {})
        assert footer["text"] == "{} of {}".format(i + 1, expected_embed_count)
